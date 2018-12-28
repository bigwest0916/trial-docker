from django.shortcuts import render
from django.http import HttpResponse
from hs.models import QuestionVersionMaster, CategoryMaster, QuestionMaster, DiagnosisMaster, RegistResult
from django.template import loader
from django.db.models import Max
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import re


# Create your views here
def index(request):
	template = loader.get_template('hsindex.html')
	diag = DiagnosisMaster.objects.all()
	context = {
		'diag': diag,
	}
	return HttpResponse(template.render(context, request))


def create(request, diagnosis_id):
	# 質問の表示
	if request.method == 'GET':
		q = RegistResult.objects.filter(diagnosismaster_id=diagnosis_id)
		template = loader.get_template('hs_list.html')

		# 初めて回答する場合
		if q.count() == 0:
			max_version = QuestionVersionMaster.objects.all().aggregate(
				Max('id'))
			categories = CategoryMaster.objects.filter(
				questionversionmaster__id=max_version["id__max"])

			context = {
				'max_hs_version': max_version["id__max"],
				'diagnosis_id': diagnosis_id,
				'categories': categories
			}

			return HttpResponse(template.render(context, request))

	# ヒアリングシート初回登録処理
	else:
		template = loader.get_template('finish.html')

		version = request.POST.get("version")
		diagnosis_id = request.POST.get("diagnosis_id")

		for key in request.POST:
			if key != 'csrfmiddlewaretoken' and key != 'diagnosis_id' and key != 'version':

				vm = QuestionVersionMaster.objects.get(pk=version)
				dm = DiagnosisMaster.objects.get(
					pk=request.POST["diagnosis_id"])
				cm = QuestionMaster.objects.get(pk=key).categorymaster
				qm = QuestionMaster.objects.get(pk=key)

				if qm.required_flg == 1:
					if not request.POST[key]:
						messsage = '必須入力がありません'
						return render(request, 'finish.html', message)

				if qm.form_type == 2:
					answer_value = ','.join(request.POST.getlist(key))
				else:
					answer_value = request.POST[key]

				r = RegistResult.objects.update_or_create(
					questionversionmaster=vm,
					diagnosismaster=dm,
					categorymaster=cm,
					questionmaster=qm,
					answer=answer_value,
					defaults={
						'questionversionmaster': vm,
						'diagnosismaster': dm,
						'categorymaster': cm,
						'questionmaster': qm,
					}
					# categorymaster=QuestionMaster.objects.get(pk=key).categorymaster.id,
				)

		return render(request, 'finish.html')


def change(request, diagnosis_id):
	# 入力画面を標示する場合
	if request.method == 'GET':
		q = RegistResult.objects.filter(diagnosismaster_id=diagnosis_id)
		version = q[0].questionversionmaster_id
		template = loader.get_template('hs_list2.html')

		# 二回目以降回答する場合
		if q.count() != 0:

			# 特定診断の回答群を取得
			categories = CategoryMaster.objects.filter(
				questionversionmaster__id=version)
			cm = []
			for category in categories:
				qms = category.questionmaster_set.filter(
					categorymaster=category)
				qm = []
				for q in qms:
					try:
						qm.append({'q': q, 'r': q.registresult_set.get(
							diagnosismaster=diagnosis_id)}, )
					except ObjectDoesNotExist:
						qm.append({'q': q, 'r': ''}, )
				cm.append({'category': category, 'qm': qm}, )

			context = {
				'version': version,
				'diagnosis_id': diagnosis_id,
				'categories': cm,
			}

			return HttpResponse(template.render(context, request))

		else:
			return HttpResponse("エラー")


	# 回答修正登録する場合
	else:
		version = request.POST.get("version")
		diagnosis_id = request.POST.get("diagnosis_id")
		context={}
		for key in request.POST:
			if not key in ('csrfmiddlewaretoken', 'version', 'diagnosis_id'):
				messages = []
				answer_value = ','.join(request.POST.getlist(key))

				# 必須チェック(required_flg == 1、 かつ、answer_value == '')
				if RegistResult.objects.get(
						id=key).questionmaster.required_flg == 1 and answer_value == '':
					messages.append('必須チェックエラー:質問番号'+str(key))
				else:
					pass

				# 入力内容チェック
				# 回答のform_typeが2：checkbox、3：radio、5：selectの場合
				if RegistResult.objects.get(id=key).questionmaster.form_type in (2, 3, 5):
					if answer_value not in RegistResult.objects.get(id=key).questionmaster.answer_values_as_list():
						messages.append('入力内容チェックエラー:質問番号'+str(key))

				# 回答のform_typeが1：textの場合
				elif RegistResult.objects.get(id=key).questionmaster.form_type in (1,):
					# 文字数チェック
					if len(answer_value) > RegistResult.objects.get(id=key).questionmaster.answer_len:
						messages.append('文字数チェックエラー:質問番号'+str(key))
					else:
						pass

					# 文字形式チェック
					pattern = RegistResult.objects.get(id=key).questionmaster.answer_regex
					repatter = re.compile(pattern)

					if not repatter.match(answer_value):
						messages.append('文字形式チェックエラー:質問番号'+str(key))




				# 回答のform_typeが1,2,3,5,26以外の場合
				else:
					pass

				# バリデーションエラーが発生した場合の処理
				if len(messages) != 0:
					template = loader.get_template('regerror.html')
					context={
						'messages':messages
					}
					return HttpResponse(template.render(context, request))

				# 入力値に問題がなかった場合の処理
				else:
					template = loader.get_template('finish.html')
					context={'message': '登録が完了いたしました。','remote':request.META["REMOTE_ADDR"],'answer':answer_value}
					# 回答更新
					RegistResult.objects.filter(pk=key).update(answer=answer_value)

		return HttpResponse(template.render(context, request))



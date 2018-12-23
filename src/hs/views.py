from django.shortcuts import render
from django.http import HttpResponse
from hs.models import QuestionVersionMaster,CategoryMaster,QuestionMaster,DiagnosisMaster,RegistResult
from django.template import loader
from django.db.models import Max
from django.shortcuts import redirect



# Create your views here
def index(request):
	template = loader.get_template('hsindex.html')
	diag = DiagnosisMaster.objects.all()
	context = {
		'diag': diag,
	}
	return HttpResponse(template.render(context, request))


def create(request, diagnosis_id):

	#質問の表示
	if request.method == 'GET':
		q = RegistResult.objects.filter(diagnosismaster_id=diagnosis_id)

		#初めて回答する場合
		if q.count()==0:
			template = loader.get_template('hs_list.html')
			max_version = QuestionVersionMaster.objects.all().aggregate(Max('id'))
			categories = CategoryMaster.objects.filter(questionversionmaster__id=max_version["id__max"])

			context = {
				'max_hs_version':max_version["id__max"],
				'diagnosis_id':diagnosis_id,
				'categories':categories
			}





		# ２回め以降回答する場合
		else:

			template = loader.get_template('hs_list2.html')

			# 特定診断の回答群を取得
			rr = RegistResult.objects.filter(diagnosismaster=diagnosis_id)
			grp = rr.values('categorymaster').annotate(max=Max('categorymaster'))
			version = rr[0].questionversionmaster.id

			c_ids = []
			for g in grp:
				c_ids.append(g['categorymaster'])

			categories = []
			for c_id in c_ids:
				categories.append(
					{'category': CategoryMaster.objects.get(pk=c_id), 'rr': rr.filter(categorymaster=c_id)})

			context = {
				'version':version,
				'diagnosis_id':diagnosis_id,
				'categories':categories,
			}


		return HttpResponse(template.render(context, request))



	# ヒアリングシート登録処理
	else:
		template = loader.get_template('finish.html')

		version=request.POST.get("version")
		diagnosis_id = request.POST.get("diagnosis_id")

		for key in request.POST:
			if key != 'csrfmiddlewaretoken' and key != 'diagnosis_id' and key != 'version':

				vm = QuestionVersionMaster.objects.get(pk=version)
				dm = DiagnosisMaster.objects.get(pk=request.POST["diagnosis_id"])
				cm = QuestionMaster.objects.get(pk=key).categorymaster
				qm = QuestionMaster.objects.get(pk=key)

				if qm.required_flg==1:
					if not request.POST[key]:
						messsage='必須入力がありません'
						return render(request, 'finish.html',message)




				if qm.form_type == 2:
					answer_value=','.join(request.POST.getlist(key))
				else:
					answer_value=request.POST[key]





				r= RegistResult.objects.update_or_create(
					questionversionmaster=vm,
					diagnosismaster=dm,
					categorymaster=cm,
					questionmaster=qm,
					answer=answer_value,
					defaults={
						'questionversionmaster':vm,
						'diagnosismaster':dm,
						'categorymaster':cm,
						'questionmaster':qm,
					}
					#categorymaster=QuestionMaster.objects.get(pk=key).categorymaster.id,
				)

		return render(request,'finish.html')




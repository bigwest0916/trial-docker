from django.http import HttpResponse
from questionnaire.models import QuestionVersion, Category, Question, Answer, Diagnosis
from users.models import User, Department

from django.template import loader
from django.db.models import Max
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required
def index(request):
	template = loader.get_template('hsindex.html')
	version_kind = QuestionVersion.objects.all()
	para=request.GET.get('version')

	if request.method == 'GET':
		if "version" in request.GET:
			categories = Category.objects.filter(questionversion__id=para)
			context = {
				'version_kind': version_kind,
				'categories': categories,
				'para':para,
			}
			return HttpResponse(template.render(context,request))
		else:
			context = {
				'version_kind': version_kind,
			}
			return HttpResponse(template.render(context,request))
	if request.method == 'POST':
		pass

	return HttpResponse(template.render(context,request))

@login_required
def diag(request):
	template = loader.get_template('diag.html')
	diag = Diagnosis.objects.all()
	context = {
		'diag': diag,
	}
	return HttpResponse(template.render(context, request))

@login_required
def hs(request, diagnosis_id):

	answers = Answer.objects.filter(diagnosis_id=diagnosis_id)
	#ヒアリングシート　入力画面　表示処理
	if request.method == 'GET':

		# 初めてヒアリングシート登録する場合
		if answers.count() == 0:
			template = loader.get_template('hs_list.html')
			max_hs_version = QuestionVersion.objects.all().aggregate(Max('id'))
			categories = Category.objects.filter(questionversion__id=max_hs_version["id__max"])

			context = {
				'max_hs_version':max_hs_version["id__max"],
				'diagnosis_id':diagnosis_id,
				'categories':categories
			}

			return HttpResponse(template.render(context, request))








		# 二回目以降ヒアリングシート登録する場合
		else:
			template = loader.get_template('hs2.html')
			answer = Answer.objects.filter(diagnosis__id=diagnosis_id).first()
			question = Question.objects.filter(id=answer.question_id).first()
			category = Category.objects.filter(id=question.category_id).first()
			qv = QuestionVersion.objects.filter(id=category.questionversion_id).first()
			categories = Category.objects.filter(questionversion=qv.id)
			context = {
				'diagnosis_id':diagnosis_id,
				'categories':categories
			}

			return HttpResponse(template.render(context, request))


















	#ヒアリングシート　登録処理
	else:
		#

		uid = request.session.get('_auth_user_id')
		user_id = uid.translate(str.maketrans({'-': ''}))
		user = User.objects.get(pk=user_id)

		version=request.POST.get("version")
		categories=Category.objects.filter(questionversion__id=version)


		for category in categories:
			for q in category.question_set.all():
				Answer.objects.update_or_create(
					question = q,
					diagnosis = Diagnosis.objects.get(pk=request.POST.get("diagnosis_id")),
					#user=request.session.get('_auth_user_id'),
					user = user,
					answer = request.POST.get(str(q.id)),
					updated_by = "dummy",
				)
		return HttpResponse(uid)


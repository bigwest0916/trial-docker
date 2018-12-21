from django.shortcuts import render
from django.http import HttpResponse
from hs.models import QuestionVersionMaster,CategoryMaster,QuestionMaster,DiagnosisMaster,Question,Answer
from django.template import loader
from django.db.models import Max



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
		q = Question.objects.filter(diagnosismaster_id=diagnosis_id)
		template = loader.get_template('hs_list.html')

		#初めて回答する場合
		if q.count()==0:
			max_version = QuestionVersionMaster.objects.all().aggregate(Max('id'))
			categories = CategoryMaster.objects.filter(questionversionmaster__id=max_version["id__max"])

			context = {
				'max_hs_version':max_version["id__max"],
				'diagnosis_id':diagnosis_id,
				'categories':categories
			}

			return HttpResponse(template.render(context, request))

		# ２回め以降回答する場合
		else:
			pass


	# ヒアリングシート登録処理
	else:
		version=request.POST.get("version")
		diagnosis_id = request.POST.get("diagnosis_id")
		for key in request.POST:
			if key != 'csrfmiddlewaretoken' and key != 'diagnosis_id' and key != 'version':

				vm = QuestionVersionMaster.objects.get(pk=version)
				dm = DiagnosisMaster.objects.get(pk=request.POST["diagnosis_id"])
				cm = QuestionMaster.objects.get(pk=key).categorymaster
				qm = QuestionMaster.objects.get(pk=key)

				q= Question.objects.update_or_create(
					questionversionmaster=vm,
					diagnosismaster=dm,
					categorymaster=cm,
					questionmaster=qm,
					#categorymaster=QuestionMaster.objects.get(pk=key).categorymaster.id,
				)

		return HttpResponse(q)

'''
				a = Answer.objects.update_or_create(
					question = q,
				)

				context={
					"key":key,
					"categorymaster":"categorymaster:"+str(QuestionMaster.objects.get(pk=str(key)).categorymaster.id),

				}
'''



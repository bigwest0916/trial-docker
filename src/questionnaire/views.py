from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from questionnaire.models import QestionVersion, Qestion, Answer

# Create your views here.

class QestionVersionList(ListView):
	model = QestionVersion

'''
	def get_queryset(self):
		query_set = QestionVersion.objects.all()
		return query_set
'''



class QestionList(ListView):
	model = Qestion

class AnswerList(ListView):
	model = Answer
from django.contrib import admin
from questionnaire.models import QuestionVersion, Category, Question, Answer, Diagnosis

# Register your models here.
@admin.register(QuestionVersion)
class QestionVersionAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    pass
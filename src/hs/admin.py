from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(QuestionVersionMaster)
class QestionVersionAdmin(admin.ModelAdmin):
    pass

@admin.register(CategoryMaster)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestionMaster)
class QestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(DiagnosisMaster)
class DiagnosisAdmin(admin.ModelAdmin):
    pass

@admin.register(RegistResult)
class DiagnosisAdmin(admin.ModelAdmin):
    pass

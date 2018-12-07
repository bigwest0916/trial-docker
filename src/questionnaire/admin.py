from django.contrib import admin
from questionnaire.models import QestionVersion, Qestion, Answer

# Register your models here.
@admin.register(QestionVersion)
class QestionVersionAdmin(admin.ModelAdmin):
    pass

@admin.register(Qestion)
class QestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
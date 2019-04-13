from django.contrib import admin
from .models import Questions, Answers, QuestionGroups

# Register your models here.

class AnswerInline(admin.TabularInline):
    model=Answers

class QuestionsAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]
    class Meta:
        model=Questions

class QuestionGroupsAdmin(admin.ModelAdmin):
    class Meta:
        model=QuestionGroups

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(QuestionGroups, QuestionGroupsAdmin)

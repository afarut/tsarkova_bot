from django.contrib import admin
from django.db import models
from .models import Question, Answer, Filter, TelegramUser
from django.forms import CheckboxSelectMultiple


admin.site.register(Answer)
admin.site.register(TelegramUser)


class FilterInline(admin.TabularInline):
    model = Question.filters.through
    extra = 0
    can_delete = False
    show_change_link = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [FilterInline]


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
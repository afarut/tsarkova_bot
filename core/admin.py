from django.contrib import admin
from .models import Question, Answer, Filter, TelegramUser
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Filter)
admin.site.register(TelegramUser)
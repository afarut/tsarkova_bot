from django.contrib import admin
from .models import Question, Answer, Filter, TelgramUser
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Filter)
admin.site.register(TelgramUser)
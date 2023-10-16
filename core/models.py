from django.db import models
from .constants import VERBOSE_MARK_TYPE
from datetime import datetime
from django.utils import timezone


class Question(models.Model):
	text = models.TextField(max_length=500)
	answer = models.TextField(max_length=700)

	def __str__(self):
		return self.text


class Answer(models.Model):
	telegram_id = models.IntegerField()
	mark = models.PositiveIntegerField(choices=VERBOSE_MARK_TYPE, default=4)
	datetime = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

	def __str__(self):
		return f"{self.telegram_id}:{self.mark}"
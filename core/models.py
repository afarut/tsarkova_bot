from django.db import models
from .constants import VERBOSE_MARK_TYPE
from datetime import datetime
from django.utils import timezone


class Question(models.Model):
	text = models.TextField(max_length=500, unique=True)
	answer = models.TextField(max_length=900)
	image = models.ImageField(upload_to="questions", null=True, blank=True)

	def __str__(self):
		return self.text

	def get_image(self):
		if self.image:
			return open(self.image.path, "rb")
		return None


class Answer(models.Model):
	telegram_id = models.IntegerField()
	mark = models.PositiveIntegerField(choices=VERBOSE_MARK_TYPE, default=4)
	datetime = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

	def __str__(self):
		return f"{self.telegram_id}:{self.mark}"


class Filter(models.Model):
	name = models.CharField(max_length=15)
	questions = models.ManyToManyField(Question, related_name="filters")

	def __str__(self):
		return self.name


def get_default_filter():
	default_filter = Filter.objects.get_or_create(name="Все вопросы")[0]
	for question in Question.objects.all():
		default_filter.questions.add(question)
	return default_filter


class TelegramUser(models.Model):
	telegram_id = models.PositiveIntegerField(unique=True)
	selected_filter = models.ForeignKey(Filter, on_delete=models.SET(get_default_filter), default=get_default_filter)
	username = models.CharField(max_length=200, null=True, blank=True)
	name = models.CharField(max_length=200, default="Аноним (default value)")

	def __str__(self):
		return self.name
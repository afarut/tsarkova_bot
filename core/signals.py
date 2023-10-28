from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Filter, Question



@receiver(post_save, sender=Question)
def autoposting_receiver(sender, instance, created, *args, **kwargs):
    if created:
        ft = Filter.objects.get_or_create(name="Все вопросы")[0]
        ft.questions.add(instance)
        ft.save()
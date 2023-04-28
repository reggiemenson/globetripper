from django.db.models.signals import post_save
from django.dispatch import receiver
from models import User
from travels.utils import recalculate_platform_badges


@receiver(post_save, sender=User)
def platform_recalculation(sender, **kwargs):
    # TODO: Test view behaviour, possible optimisation here
    recalculate_platform_badges()

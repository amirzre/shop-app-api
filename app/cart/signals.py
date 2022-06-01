from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from cart.models import Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)

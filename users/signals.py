from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Client
import uuid

@receiver(post_save, sender=Client)
def send_activation_code(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        code = uuid.uuid4().hex
        instance.activation_code = code
        instance.save(update_fields=["activation_code"])
        send_mail(
            "Activation code",
            f"Your code: {code}",
            "webmaster@localhost",
            [instance.email],
        )

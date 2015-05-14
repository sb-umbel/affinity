import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Brand(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=256)
    created = AutoCreatedField()
    modified = AutoLastModifiedField()


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    brands = models.ManyToManyField(Brand, related_name='profiles')
    created = AutoCreatedField()
    modified = AutoLastModifiedField()


@receiver(signals.post_save, sender=Brand)
def touch_brand_profiles(sender, instance, **kwargs):
    instance.profiles.update(modified=timezone.now())


@receiver(signals.m2m_changed, sender=Profile.brands.through)
def touch_profile_brand(sender, instance, **kwargs):
    instance.save(update_fields=['modified'])

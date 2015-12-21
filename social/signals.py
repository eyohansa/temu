from django.db.models.signals import post_save
from django.dispatch import receiver
from social.models import TemuUser, Relationship

import logging


logger = logging.getLogger(__name__)


@receiver(post_save, sender=TemuUser, dispatch_uid="create_user_relationship")
def user_relationship_handler(sender, instance, created, using, **kwargs):

    if created:
        r = Relationship(user=instance)
        r.save(using=using)

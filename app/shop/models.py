from django.db import models
from accounts.models import User, UserProfile


def shop_docs(instance, filename):
    return 'docs/{0}/{1}'.format(instance.user.id, filename)


class Shop(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    shop_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    docs = models.FileField(upload_to=shop_docs)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name

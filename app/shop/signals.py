# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils.text import slugify
# from django.core.exceptions import ValidationError
# from django.contrib import messages

# from .models import Item, Category


# @receiver(pre_save, sender=Item)
# def pre_save_update_slug_item(sender, instance, **kwargs):
#     """
#     Generates a slug for the Item instance before saving it.
#     """
#     if not instance.slug:
#         if instance.id is None:
#             # Instance has not yet been saved,
#  so we use `None` as a placeholder for `id`
#             instance.slug = slugify(instance.name)
#         else:
#             instance.slug = slugify(instance.name + '-' + str(instance.id))
#     else:
#         # if slug is set - check if it is unique
#         slug = instance.slug
#         if Item.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
#             raise ValidationError('The slug "%s" is already in use.' % slug)


# @receiver(pre_save, sender=Category)
# def pre_save_update_slug_item(sender, instance, **kwargs):
#     """
#     Generates a slug for the Item instance before saving it.
#     """
#     slug = slugify(instance.name+'-'+str(instance.shop.id))
#     if not Category.objects.filter(slug=slug):
#         instance.slug = slug
#     else:
#         raise ValidationError('The slug "%s" is already in use.' % slug)

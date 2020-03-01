import os

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.db.models import FileField


class Command(BaseCommand):
    help = "This command deletes all media files from the MEDIA_ROOT directory which are no longer referenced by any of the models from installed_apps"

    def handle(self, *args, **options):
        all_models = apps.get_models()
        physical_files = set()
        db_files = set()

        # Get all files from the database
        for model in all_models:
            file_fields = []
            filters = Q()
            for f_ in model._meta.fields:
                if isinstance(f_, FileField):
                    file_fields.append(f_.name)
                    is_null = {'{}__isnull'.format(f_.name): True}
                    is_empty = {'{}__exact'.format(f_.name): ''}
                    filters &amp;= Q(**is_null) | Q(**is_empty)
            # only retrieve the models which have non-empty, non-null file fields
            if file_fields:
                files = model.objects.exclude(filters).values_list(*file_fields, flat=True).distinct()
                db_files.update(files)

        # Get all files from the MEDIA_ROOT, recursively
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root is not None:
            for relative_root, dirs, files in os.walk(media_root):
                for file_ in files:
                    # Compute the relative file path to the media directory, so it can be compared to the values from the db
                    relative_file = os.path.join(os.path.relpath(relative_root, media_root), file_)
                    physical_files.add(relative_file)

        # Compute the difference and delete those files
        deletables = physical_files - db_files
        if deletables:
            for file_ in deletables:
                os.remove(os.path.join(media_root, file_))

            # Bottom-up - delete all empty folders
            for relative_root, dirs, files in os.walk(media_root, topdown=False):
                for dir_ in dirs:
                    if not os.listdir(os.path.join(relative_root, dir_)):
                        os.rmdir(os.path.join(relative_root, dir_))

##=================================================================
## WITH SIGNALS

from django.db.models import FileField
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver

LOCAL_APPS = [
    'my_app1',
    'my_app2',
    '...'
]

def delete_files(files_list):
    for file_ in files_list:
        if file_ and hasattr(file_, 'storage') and hasattr(file_, 'path'):
            # this accounts for different file storages
            # (e.g. when using django-storages)
            storage_, path_ = file_.storage, file_.path
            storage_.delete(path_)

@receiver(post_delete)
def handle_files_on_delete(sender, instance, **kwargs):
    # presumably you want this behavior only for your apps,
    # in which case you will have to specify them
    is_valid_app = sender._meta.app_label in LOCAL_APPS
    if is_valid_app:
        files_list = [getattr(instance, field_.name, None) for field_ in sender._meta.fields if isinstance(field_, FileField)]
        delete_files(files_list)

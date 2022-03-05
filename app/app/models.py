from django.db import models
from django.utils.translation import gettext_lazy as _

from .tasks import translate_doc, translate_text
from .utils import generate_secret
# Create your models here.


class CommonInfo(models.Model):
    LANGUAGES = (
        ('en', _('English')),
        ('tr', _('Turkish'))
    )

    source_language = models.CharField(max_length=5, choices=LANGUAGES)
    target_language = models.CharField(max_length=5, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True)
    miscellaneous = models.TextField(blank=True)

    class Meta:
        abstract = True


class Segment(CommonInfo):
    source = models.TextField()
    reviewed_source = models.TextField(blank=True)
    target = models.TextField(blank=True)
    reviewed_target = models.TextField(blank=True)
    user_edited_target = models.TextField(blank=True)

    class Meta:
        ordering = ['-id']


class File(CommonInfo):
    source_file = models.FileField(upload_to='app/files/', blank=True)
    bilingual_file = models.FileField(upload_to='app/files/')

    def delete(self, *args, **kwargs):
        if self.source_file:
            self.source_file.delete()
        self.bilingual_file.delete()
        super().delete()

class TranslationQuery(CommonInfo):
    STATUSES = (
        (1, _('New')),
        (2, _('Processing')),
        (3, _('Ready'))
    )

    content = models.JSONField()
    secret = models.CharField(max_length=8, unique=True, default=generate_secret)
    status = models.IntegerField(choices=STATUSES, default=1)

    def save(self, no_override=False, *args, **kwargs):
        super().save(*args, **kwargs)
        if no_override:
            return
        elif self.status == 1:
            self.status = 2
            self.save(no_override=True)

            if self.content['type'] == 'doc':
                translate_doc.delay(self.content['file_id'], self.id)
            else:
                translate_text.delay(self.content['text'], self.id)

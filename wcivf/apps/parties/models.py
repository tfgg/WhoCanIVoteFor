import os

import requests

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify


class PartyManager(models.Manager):
    def update_or_create_from_ynr(self, party):
        defaults = {
            'party_name': party['name']
        }

        party_obj, _ = self.update_or_create(
            party_id=party['id'],
            defaults=defaults
        )
        if party['images']:
            same_photo = False

            selected_image = party['images'][0]
            for image in party['images']:
                if image['is_primary']:
                    selected_image = image

            photo_filename = selected_image['image_url'].split('/')[-1]

            url = "{}{}".format(settings.YNR_BASE, selected_image['image_url'])

            try:
                file_path = party_obj.emblem.file.name
            except:
                file_path = None

            # This person has a photo already, check if it's the same
            if file_path and os.path.exists(file_path):
                if party_obj.emblem.name.endswith(photo_filename):
                    same_photo = True

            if not same_photo:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(requests.get(url).content)
                img_temp.flush()

                party_obj.emblem.save(photo_filename, File(img_temp))
                party_obj.save()

        return (party_obj, _)


class Party(models.Model):
    """
    Represents a UK political party.
    """
    party_id = models.CharField(blank=True, max_length=100, primary_key=True)
    party_name = models.CharField(max_length=765)
    emblem = models.ImageField(upload_to="parties/emblems", null=True)
    wikipedia_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Parties'
        ordering = ('party_name', )

    objects = PartyManager()

    def __str__(self):
        return "%s (%s)" % (self.party_name, self.pk)

    def get_absolute_url(self):
        return reverse('party_view', args=[
            str(self.pk),
            slugify(self.party_name)
        ])

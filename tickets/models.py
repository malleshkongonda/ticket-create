from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from tickets.enums import Urgency


class Ticket(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    public = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tickets'
    )
    urgency = models.CharField(choices=Urgency.choices(), default=Urgency.LOW, max_length=20)

    def get_description(self):
        """
        If urgency high, print 3 exclamation marks instead of one.
        """
        d = self.description
        if self.urgency == Urgency.HIGH:
            d = d.replace('!', '!!!')
        return d

    def __str__(self):
        return 'Ticket #{id}'.format(id=self.id, title=self.title)

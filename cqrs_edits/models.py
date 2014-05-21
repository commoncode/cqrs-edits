from django.db import models


class EditLog(models.Model):
    '''
    Store operations from the Edits Collection
    '''
    blob = models.TextField()

    def __unicode__(self):
        return self.blob
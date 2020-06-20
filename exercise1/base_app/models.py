# -*- coding: utf-8 -*-
"""The models of the main module.

    Here we have all the models that do not fit into the logical grouping of other
    models in the project. They are shared through out the project of fulfill a
    more general requirement in the project.
"""

import uuid

from django.db import models, IntegrityError
from django.urls import reverse
from django.utils import timezone


class BaseQuerySet(models.QuerySet):
    """The queryset class used to extend the manager for the base class.

        This class enables us to define custom queryset that abstract the business logic
        to within the model layer. Hence the code can easily be used to build the app with
        consistent logic through out all the modules that use these models.

        This results in less complexity within the views and helps developers extend the project
        in a reliable and maintainable manner.
    """

    def update(self, **kwargs):
        if 'updater' in kwargs:
            kwargs['date_updated'] = timezone.now()
            super(BaseQuerySet, self).update(**kwargs)
        else:
            raise IntegrityError('Updater not specified',
                                 'When updating any instance, the updater (User instance/pk) should be provided.')

    def active(self):
        """Queryset to return only the active rows from the model.

            This queryset filters out all the model instances with is_deleted set as true.
        """
        return self.filter(is_deleted=False)

    def remove(self, updater):
        """Queryset to set the is_deleted attribute to true.

            This queryset sets the is_deleted attribute to True, which will be treated
            as a deleted instance by the remaining system.

            TO-DO:
                1. Try to extend the update method to always update the date_updated value when
                the update method is called.
        """
        return self.update(is_deleted=True, date_updated=timezone.now(), updater=updater)


class BaseModel(models.Model):
    """Base model extended by other models through out the project.

        Here we define all the common fields used by all the models used in the project.
        This way repetition is avoided and custom logic regarding these fields are abstracted
        to with  in the base model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey('auth.User', blank=True, related_name='creator_%(class)s_objects',
                                on_delete=models.PROTECT)
    updater = models.ForeignKey('auth.User', blank=True, related_name='updater_%(class)s_objects',
                                on_delete=models.PROTECT)
    date_added = models.DateTimeField(db_index=True)
    date_updated = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    objects = BaseQuerySet.as_manager()

    def __str__(self):
        return self.id


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Overriding the save methods to extend the logic.

            The date_updated and date_added attributes are set at this stage giving
            a more accurate representation of these values. Note that the update queryset
            does not call the save method and hence does not cause these modifications to
            be called. In case the update function needs to be called, please add the date_updated
            manually.

        """
        self.date_updated = timezone.now()
        if self.date_added is None:
            self.date_added = timezone.now()

        super(BaseModel, self).save(*args, **kwargs)

    def remove(self, updater):
        self.is_deleted = True
        self.updater = updater
        self.save()


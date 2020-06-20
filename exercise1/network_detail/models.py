from django.db import models

from base_app.models import BaseModel, BaseQuerySet


class NetworkDetailsQuerySet(BaseQuerySet):
    pass


class NetworkDetails(BaseModel):
    sap_id = models.CharField(max_length=18, blank=True, null=True)
    loop_back = models.CharField(max_length=15, blank=True, null=True)
    mac_address = models.CharField(max_length=17, unique=True)
    host_name = models.CharField(max_length=15, blank=True, null=True)

    objects = NetworkDetailsQuerySet.as_manager()

    class Meta:
        db_table = 'network_details'
        ordering = ['mac_address']

    def __str__(self):
        if self.mac_address:
            return "{} {}".format(self.mac_address, self.loop_back)
        else:
            return "{}".format(self.mac_address)

    def remove(self):
        self.deactivate()
        self.is_deleted = True
        self.save()

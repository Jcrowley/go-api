from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from api.authentication import ExpiringApiKeyAuthentication
from api.resources import (
    CountryResource,
    RegionResource,
    RelatedEventResource,
    DisasterTypeResource,
)
from .models import (
    ERUOwner,
    ERU,
    Heop,
    Fact,
    FactPerson,
    Rdrt,
    RdrtPerson,
)


class ERUOwnerResource(ModelResource):
    eru_set = fields.ToManyField('deployments.resources.ERUResource', 'eru_set', null=True, full=True)
    class Meta:
        queryset = ERUOwner.objects.all()
        authentication = ExpiringApiKeyAuthentication()
        resource_name = 'eru_owner'
        allowed_methods = ['get']
        filtering = {
            'country': ('exact', 'in'),
        }


class RelatedERUOwnerResource(ModelResource):
    national_society_country = fields.ForeignKey(CountryResource, 'national_society_country', full=True)
    class Meta:
        queryset = ERUOwner.objects.all()
        allowed_methods = ['get']


class ERUResource(ModelResource):
    deployed_to = fields.ForeignKey(CountryResource, 'deployed_to', full=True, null=True)
    eru_owner = fields.ForeignKey(RelatedERUOwnerResource, 'eru_owner', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    class Meta:
        queryset = ERU.objects.all()
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'eru_owner': ALL_WITH_RELATIONS,
            'type': ('exact', 'in'),
            'deployed_to': ('in', 'isnull'),
        }
        allowed_methods = ['get']


class HeopResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', null=True, full=True)
    class Meta:
        queryset = Heop.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'end_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'country': ('exact', 'in'),
            'region': ('exact', 'in'),
            'event': ('exact', 'in'),
            'dtype': ('exact', 'in'),
            'person': ('exact', 'in'),
            'role': ('exact', 'in'),
        }
        ordering = [
            'start_date',
            'end_date',
            'country',
            'region',
            'event',
            'dtype',
            'person',
            'role',
        ]


class RelatedFactPersonResource(ModelResource):
    class Meta:
        queryset = FactPerson.objects.all()
        allowed_methods = ['get']


class FactResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', null=True, full=True)
    people = fields.ToManyField('deployments.resources.RelatedFactPersonResource', 'factperson_set', null=True, full=True)
    class Meta:
        queryset = Fact.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'country': ('exact', 'in'),
            'region': ('exact', 'in'),
            'event': ('exact', 'in'),
            'dtype': ('exact', 'in'),
        }
        ordering = [
            'start_date',
            'country',
            'region',
            'event',
            'dtype',
        ]


class RelatedFactResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    class Meta:
        queryset = Fact.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()


class FactPersonResource(ModelResource):
    fact = fields.ForeignKey(RelatedFactResource, 'fact', null=True, full=True)
    class Meta:
        resource_name = 'fact_person'
        queryset = FactPerson.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'end_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'name': ('exact', 'in'),
            'role': ('exact', 'in'),
            'society_deployed_from': ('exact', 'in'),
        }
        ordering = [
            'start_date',
            'end_date',
            'name',
            'role',
            'society_deployed_from',
        ]


class RelatedRdrtPersonResource(ModelResource):
    class Meta:
        queryset = RdrtPerson.objects.all()
        allowed_methods = ['get']


class RdrtResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    dtype = fields.ForeignKey(DisasterTypeResource, 'dtype', null=True, full=True)
    people = fields.ToManyField('deployments.resources.RelatedRdrtPersonResource', 'rdrtperson_set', null=True, full=True)
    class Meta:
        queryset = Rdrt.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'country': ('exact', 'in'),
            'region': ('exact', 'in'),
            'event': ('exact', 'in'),
            'dtype': ('exact', 'in'),
        }
        ordering = [
            'start_date',
            'country',
            'region',
            'event',
            'dtype',
        ]


class RelatedRdrtResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country', full=True)
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    event = fields.ForeignKey(RelatedEventResource, 'event', null=True, full=True)
    class Meta:
        queryset = Rdrt.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()


class RdrtPersonResource(ModelResource):
    rdrt = fields.ForeignKey(RelatedRdrtResource, 'rdrt', null=True, full=True)
    class Meta:
        resource_name = 'rdrt_person'
        queryset = RdrtPerson.objects.all()
        allowed_methods = ['get']
        authentication = ExpiringApiKeyAuthentication()
        filtering = {
            'start_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'end_date': ('gt', 'gte', 'lt', 'lte', 'range', 'year', 'month', 'day'),
            'name': ('exact', 'in'),
            'role': ('exact', 'in'),
            'society_deployed_from': ('exact', 'in'),
        }
        ordering = [
            'start_date',
            'end_date',
            'name',
            'role',
            'society_deployed_from',
        ]

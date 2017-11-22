from django.db import models


class DisasterType(models.Model):
    """ Type of disaster """
    name = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    """ A disaster, which could cover multiple countries """

    eid = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    dtype = models.ForeignKey(DisasterType, null=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=20, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def countries(self):
        """ Get countries from all appeals and field reports in this disaster """
        countries = [country for fr in self.fieldreport_set.all() for country in fr.countries.all()] + \
                    [appeal.country for appeal in self.appeal_set.all()]
        return list(set([c.name for c in countries]))

    def start_date(self):
        """ Get start date of first appeal """
        return min([a['start_date'] for a in self.appeal_set.all()])

    def end_date(self):
        """ Get latest end date of all appeals """
        return max([a['end_date'] for a in self.appeal_set.all()])

    def __str__(self):
        return self.name


class Country(models.Model):
    """ A country """

    name = models.CharField(max_length=100)
    iso = models.CharField(max_length=2, null=True)
    society_name = models.TextField(default="")

    def __str__(self):
        return self.name


class Document(models.Model):
    """ A document, located somwehere """

    name = models.CharField(max_length=100)
    uri = models.TextField()

    def __str__(self):
        return self.name


class Appeal(models.Model):
    """ An appeal for a disaster and country, containing documents """

    # appeal ID, assinged by creator
    aid = models.CharField(max_length=20)
    name = models.TextField(null=True)
    summary = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    event = models.ForeignKey(Event, null=True)
    country = models.ForeignKey(Country, null=True)
    sector = models.CharField(max_length=100, blank=True)

    num_beneficiaries = models.IntegerField(default=0)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_funded = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    # documents = models.ManyToManyField(Document)

    def __str__(self):
        return self.aid


class FieldReport(models.Model):
    """ A field report for a disaster and country, containing documents """

    rid = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True, default='')
    dtype = models.ForeignKey(DisasterType)
    event = models.ForeignKey(Event, null=True)
    countries = models.ManyToManyField(Country)
    status = models.IntegerField(default=0)
    request_assistance = models.BooleanField(default=False)

    num_injured = models.IntegerField(null=True)
    num_dead = models.IntegerField(null=True)
    num_missing = models.IntegerField(null=True)
    num_affected = models.IntegerField(null=True)
    num_displaced = models.IntegerField(null=True)
    num_assisted_gov = models.IntegerField(null=True)
    num_assisted_rc = models.IntegerField(null=True)
    num_localstaff = models.IntegerField(null=True)
    num_volunteers = models.IntegerField(null=True)
    num_expats_delegates = models.IntegerField(null=True)

    # action IDs - other tables?
    action = models.TextField(blank=True, default='')

    # contacts
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rid


class Service(models.Model):
    """ A resource that may or may not be deployed """

    name = models.CharField(max_length=100)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    deployed = models.BooleanField(default=False)
    location = models.TextField()

    def __str__(self):
        return self.name

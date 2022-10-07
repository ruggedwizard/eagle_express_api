from django.db import models
import uuid
from django.contrib.auth.models import User

class ParcelPickup(models.Model):
    """ PARCEL PICKUP MODEL"""
    OPTIONS = (
        ('PICKED UP','PICKED UP'),
        ('REQUESTED','REQUESTED')
    )

    lastname = models.CharField(max_length=200, null=False, blank=False)
    firstname = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=400,null=False,blank=False)
    phone_number = models.CharField(null=True,blank=True,default="Null Provided",max_length=200)
    nearest_landmark = models.CharField(max_length=250,null=False,blank=False)
    parcel_type = models.CharField(max_length=250,null=False,blank=False)
    parcel_weight = models.CharField(max_length=200,null=True,blank=True)
    alternative_phone = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(choices=OPTIONS,max_length=100,help_text="options PICKED UP and REQUESTED", default="REQUESTED")
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.firstname + " " +self.lastname + " Parcel"


class Partner(models.Model):
    """PARTNER MODEL"""
    # VERIFICATION OPTIONS
    VERIFIED_STATUS = (
        ('NOT VERIFIED','NOT VERIFIED'),
        ('VERIFIED','VERIFED')
    )

    company_name = models.CharField(max_length=200,null=False,blank=False)
    company_email = models.CharField(max_length=200,null=False, blank=False,unique=True)
    company_address = models.CharField(max_length=3200,null=False,blank=False, unique=True)
    owners_name = models.CharField(max_length=200,null=True,blank=False)
    owners_address = models.CharField(max_length=200,null=False,blank=False)
    owners_phone = models.CharField(max_length=200,null=False,blank=False)
    verification_status = models.CharField(max_length=200, choices=VERIFIED_STATUS,help_text="options NOT VERIFIED and VERIFIED, default is NOT VERIFIED", default="NOT VERIFIED")
    logistic_type = models.CharField(max_length=200, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator',)

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.company_name + "'s " + self.verification_status


class Park(models.Model):
    """
    PARK MODEL
    """
    park_name = models.CharField(max_length=200, null=False, blank=False)
    park_address = models.CharField(max_length=3500,null=False,blank=False)
    park_local_govt_area = models.CharField(max_length=200, null=False,blank=False)
    park_state = models.CharField(max_length=200, null=False,blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner')

    class Meta:
        ordering = ['date_added']
    
    def __str__(self):
        return self.park_name


class Parcel(models.Model):
    """PARCEL MODEL READY PICKED FOR DELIVERY"""
    STATUS = (
        ('DELIVERED','DELIVERED'),
        ('SENT FOR DELIVERY','SENT FOR DELIEVRY'),
        ('IN TRANSIT', 'IN TRANSIT'),
        ('FAILED TO DELIVER', 'FAILED TO DELIVER'),
        ('RECEIVED FOR DELIEVRY', 'RECEIVED FOR DELIVERY')
    )

    tracking_id = models.UUIDField(default=uuid.uuid4,editable=False)
    parcel = models.ForeignKey(ParcelPickup,on_delete=models.CASCADE)
    current_location = models.ForeignKey(Park,on_delete=models.CASCADE, help_text="Indicate your current Park Location")
    riders_contact = models.CharField(max_length=200,null=False,blank=False,help_text="Please Add a Rider Conatct")
    parcel_status = models.CharField(max_length=200,choices=STATUS,default="RECEIVED FOR DELIEVRY")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_created']
    def __str__(self):
        return self.parcel_status

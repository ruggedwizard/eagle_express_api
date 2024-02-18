# EAGLE EXPRESS API
## ABOUT THE API
The API can serve for both mobile and web based solution for logistic service which allows for various, logistic companies move parcels and also allow the owner of the parcel track their parcel. 
Logistics company can register to partner with each other i.e. a logistic company can pick up a percel, and deliver to a state they don't cover. 

### WHATS LEFT/ WHAT CAN BE ADDED

<li> Add Payment Option When a User Request Parcel Pickup
<li> Email Template Receipt, Carrying The Price and Parcel Description
<li> Push Notifications (for Mobile and Webapp)
<li> Calculating Amount for parcel based on weight and distance
<li> Canceling a Pickup Request


### RUNNING THE CODE
```
 CLONE THE REPOSITORY AND SETUP A VIRTUAL ENVIRONMENT TO RUN THE PROJECT, LIVE API AT 

```
## API USEAGE

A SWAGGER UI is also added at {{BASE_URL}}/swagger
### AUTHENTICATION - LOGIN, LOGOUT AND REGISTER 
### REGISTER ACCOUNT

{{BASE_URL}}/register
```
{
  "username": "johndoe",
  "password": "password",
  "email": "user@example.com"
}
```
>[!NOTE]
the email address is a unique field

### LOGIN USER ACCOUNT
{{BASE_URL}}/api/token
```
{
  "username": "johndoe",
  "password": "password"
}

```
This will return access token and refresh token <br>
access token: The access token has a life span of 60 MINUTES after creation <br>
refresh token: The refresh token has a life span of 1 DAY (24 Hours) <br>

### LOGOUT USER ACCOUNT
{{BASE_URL}}/api/token/blacklist/
```
{
  "refresh": "refresh_token"
}
```
blacklisting a token will disable the refresh token and its access token
>[!NOTE]
on the frontend (WEB/MOBILE) the refresh and access token should be removed from the local storage as well

### REFRESHING A TOKEN
{{BASE_URL}}/api/token/refresh/
```
{
  "refresh": "string"
}
```
Takes a refresh type JSON web token and returns an access type JSON web <br>
token if the refresh token is valid.
<div id="parks">

### PARKS ENDPOINT
### LIST ALL PARKS

</div>

{{BASE_URL}}/parks/


### ADD PARK (ACCESS TOKEN REQUIRED)
{BASE_URL}/parks/

```
{
  "park_name": "string",
  "park_address": "string",
  "park_local_govt_area": "string",
  "park_state": "string"
}
```

### GET A SINGLE PARK DATA AND  DELETE PARK
{{BASE_URL}}/parks/{{PARK_ID}}

>[!NOTE]
only the creator of a park can modify a park record, and delete record

### UPDATE PARK DATA
{{BASE_URL}}/parks/{{PARK_ID}}
```
{
  "park_name": "string",
  "park_address": "string",
  "park_local_govt_area": "string",
  "park_state": "string"
}
```

### PARTNERS ENDPOINT
### LIST ALL PARTNERS
{{BASE_URL}}/partners/

### ADD A PARTNER ACCOUNT
{{BASE_URL}}/partners/
```
{
  "company_name": "string",
  "company_email": "string",
  "company_address": "string",
  "owners_name": "string",
  "owners_address": "string",
  "owners_phone": "string",
  "verification_status": "NOT VERIFIED",
  "logistic_type": "string"
}
```
### GET A SINGLE PARTNER DATA AND  DELETE PARTNER DATA 
{{BASE_URL}}/partners/{{PARTNER_ID}}

>[!NOTE]
A PARTNER RECORD CAN BE DELETED, AND UPDATED

<div id="parcels">

## PARCEL PICKUP & TRACKING
### LSIT ALL PARCELS

</div>
{{BASE_URL}}/parcel-pickup/

### REQUEST FOR A PERCEL TO BE PICKUP
{{BASE_URL}}/parcel-pickup/
```
{
  "lastname": "string",
  "firstname": "string",
  "email": "string",
  "phone_number": "string",
  "nearest_landmark": "string",
  "parcel_type": "string",
  "parcel_weight": "string",
  "alternative_phone": "string",
  "status": "PICKED UP (OPTIONAL, Which will default to REQUESTED)"
}
```

### DELETE A PICKUP RECORD, UPDATE AND DELETE PICKUP RECORD
{{BASE_URL}}/parcel-pickup/{{id}}

This will allow parcel data being modified maybe due to error in weight record and delete a record or parcel 

## AFTER PARCEL IS PICKED UP AND READY TO BE DELIVERED
### LIST ALL PARCELS PICKED UP
{{BASE_URL}}/parcels/

### ASSIGN RIDERS AND PICKUP POINTS FOR A PARCEL, ASSIGNING TRACKING NUMBER e.t.c
```
{
  "riders_contact": "string",
  "parcel_status": "DELIVERED",
  "parcel": {
    "lastname": "string",
    "firstname": "string",
    "email": "string",
    "phone_number": "string",
    "nearest_landmark": "string",
    "parcel_type": "string",
    "parcel_weight": "string",
    "alternative_phone": "string",
    "status": "PICKED UP"
  },
  "current_location": {
    "park_name": "string",
    "park_address": "string",
    "park_local_govt_area": "string",
    "park_state": "string"
  }
}
```

>[!NOTE]
both parcel and current location are based on data already entered as <b> <a href="#parcels"> PARCEL </a></b> and  <b> <a href="#parks"> PARKS</a> <b> Data respectively

### UPDATE STATUS OF PARCEL
{{BASE_URL}}/parcels/{{parcel_id}}



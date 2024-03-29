from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from express.permisions import IsOwnerOrReadOnly
from express.serializers import LogoutSerializer, ParcelPickupSerializer, ParkSerializer, PatnerSerializer, ParcelSerializer, RegisterSerializer, UserSerializer
from express.models import ParcelPickup, Park,Partner,Parcel
from express.emails import send_email, update_email
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime




@api_view(['GET'])
def index_route(request):
    now = datetime.now()

    return Response({
        'message':f'Welcome, and the server time is {now.strftime("%H:%M:%S")}'
    })

@swagger_auto_schema(method = 'POST',request_body=ParcelPickupSerializer)
@api_view(['GET','POST'])
def parcel_package(request):

    """
    List all Parcel Added for Pickup
    """
    if request.method == 'GET':
        parcels = ParcelPickup.objects.all()
        serializers = ParcelPickupSerializer(parcels, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = request.data
        email = data['email']
        serializer = ParcelPickupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email(email=email)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method = 'PUT',request_body=ParcelPickupSerializer)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def parcel_detail(request,pk):
    """
    Get More Details About a Single Parcel
    """
    try:
        parcel = ParcelPickup.objects.get(pk=pk)
    except ParcelPickup.DoesNotExist:
        return Response({"message":"Parcel Does Not Exist"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ParcelPickupSerializer(parcel)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ParcelPickupSerializer(parcel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Parcel Updated","data":serializer.data},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        parcel.delete()
        return Response({f"message":"Parcel with the id of {request.pk} deleted"},status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(method='POST',request_body=PatnerSerializer)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def partners_list(request):
    """
    List Partners and Add Partners
    """
    if request.method == 'GET':
        partner = Partner.objects.all()
        serializer = PatnerSerializer(partner,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = request.data
        email = data['company_email']
        serializer = PatnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            send_email(email=email)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT',request_body=PatnerSerializer)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def partner_detail(request,pk):
    """
    Partner Detail, update and Delete
    """
    try: 
        partner = Partner.objects.get(pk=pk)
    except Partner.DoesNotExist:
        return Response({"message":"Partner Does Not Exist"},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatnerSerializer(partner)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if request.user == partner.creator:
            serializer = PatnerSerializer(partner,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permision Denied"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user == partner.creator:
            partner.delete()
            return Response({"message":"Partner Deleted"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Permision Denied"},status=status.HTTP_401_UNAUTHORIZED)
       

@swagger_auto_schema(method='POST',request_body=ParcelSerializer)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def parcel_track(request):
    """
    PARCEL STATUS AND TRACKING 
    """
    if request.method == 'GET':
        parcel = Parcel.objects.all()
        serializer = ParcelSerializer(parcel,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
       parcel = request.data
       email = parcel['parcel']['email']
       parcel_status = parcel['parcel_status']
       riders_contact = parcel['riders_contact']
       serializer = ParcelSerializer(data=parcel)
       if serializer.is_valid():
            serializer.save()
            tracking_id = serializer.data['tracking_id']
            update_email(email=email,parcel_status=parcel_status,parcel_location=parcel_status,riders_conatct=riders_contact,tracking_id=tracking_id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method ='PUT',request_body=ParcelSerializer)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
def parcel_track_detail(request,pk):
    """
    GET A SINGLE PARCEL STATUS, UPDATE AND DELETE A PARCEL
    """
    try:
        parcel = Parcel.objects.get(tracking_id=pk)
    except Parcel.DoesNotExist:
        return Response({"message":"Parcel Does Not Exist"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ParcelSerializer(parcel)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ParcelSerializer(parcel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"parcel updated"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        parcel.delete()
        return Response({'message':'Parcel Deleted'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_list(request):
    """USER LIST"""
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_detail(request,pk):
    """USER MODEL DETAIL's and Delete User"""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message":"User Does not Exist"},status=status.HTTP_404_NOT_FOUND )
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message":"user deleted successfully"},status=status.HTTP_204_NO_CONTENT)




@swagger_auto_schema(method='POST',request_body=ParkSerializer)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def parks(request):
    """
    ADD AND LIST ALL PARKS
    """
    if request.method == 'GET':
        park = Park.objects.all()
        serializer = ParkSerializer(park, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        park = request.data
        serializer = ParkSerializer(data=park)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT',request_body=ParkSerializer)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def parks_detail(request,pk):
    """
    Park detail, Update Park and Delete Parks
    """
    try:
        park = Park.objects.get(pk=pk)
    except Park.DoesNotExist:
        return Response({"message":"Park Does not exist"},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParkSerializer(park)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if request.user == park.owner:
            data = request.data
            serializer = ParkSerializer(park,data=data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permision Denied"},status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'DELETE':
        if request.user == park.owner:
            park.delete()
            return Response({"message":"Park Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"Permision Denied"},status=status.HTTP_401_UNAUTHORIZED)
       
            
        

@swagger_auto_schema(method='POST',request_body=RegisterSerializer)
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({data:serializer.data, "message":"Account Created Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST',request_body=LogoutSerializer)
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = LogoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"logout success"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)
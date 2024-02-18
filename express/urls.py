from django.urls import path,include
from . import views





urlpatterns = [ 
    path('',views.index_route),
    path("parcels-pickup/",views.parcel_package),
    path("parcels-pickup/<int:pk>/",views.parcel_detail),
    path("partners/",views.partners_list),
    path("partners/<int:pk>/",views.partner_detail),
    path("parcels/",views.parcel_track),
    path("parcels/<str:pk>/",views.parcel_track_detail), 
    path("users/",views.user_list),
    path("users/<int:pk>",views.user_detail),
    path("parks/",views.parks),
    path("parks/<str:pk>/",views.parks_detail),
    path("register/",views.register_view),
    path("logout/",views.logout_view)
]
from django.urls import path

from .views import (
    auction_gallery,
    item_details,
    create_auction,
    my_auctions,
    place_bid,
    update_bid
)


from .views import dashboard


app_name = 'auction'

urlpatterns = [
    path('auction-gallery/', auction_gallery, name='auction-gallery'),
    path('item/<str:slug>/', item_details, name='item-detail'),
    path('create-auction/', create_auction, name='create-auction'),
    path('my-auctions/', my_auctions, name='my-auctions'),
    path('item/<str:slug>/place-bid/', place_bid, name='place-bid'),
    path('item/<str:slug>/<str:hashed_id>/update-bid/',
        update_bid,
        name='update-bid'
    ),
    
    path('', dashboard, name='dashboard'),

    
]





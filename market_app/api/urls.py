from django.contrib import admin
from django.urls import path, include
from .views import MarketsView, MarketDetailView, SellersView, seller_single_view, SellerOfMarketList, ProdutViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProdutViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    path('seller/', SellersView.as_view()),
    path('seller/<int:pk>/', seller_single_view, name='seller-detail'),
    # path('product/', products_view),
]
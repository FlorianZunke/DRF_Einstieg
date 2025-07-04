from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import MarketSerializer, SellerSerializer, SellerListSerializer, ProductSerializer
from market_app.models import Market, Seller, Product
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets




class ListRetrieveViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass

class MarketsView(generics.ListCreateAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    

class SellerOfMarketList(generics.ListCreateAPIView):
    serializer_class = SellerListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        return market.sellers.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        serializer.save(markets=[market])


class ProdutViewSet(ListRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Das ist das gleiche wie das ProductViewSet 
# class ProdutViewSetOld(viewsets.ViewSet):
#     queryset = Product.objects.all()

#     def list(self, request):
#         serializer = ProductSerializer(self.queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         product = get_object_or_404(self.queryset, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     def destroy(self, request, pk=None):
#         product = get_object_or_404(self.queryset, pk=pk)
#         serializer = MarketSerializer(product)
#         product.delete()
#         return Response(serializer.data)


class MarketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

# Das ist das gleiche wie die MarketDetailView
# @api_view(['GET', 'DELETE', 'PUT'])
# def market_detail_view(request, pk):

#     if request.method == 'GET':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market, context={'request':request})
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     if request.method == 'DELETE':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market)
#         market.delete()
#         return Response(serializer.data)



class SellersView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Das ist das gleiche wie die SellersView
# @api_view(['GET', 'POST'])
# def sellers_view(request):

#     if request.method == 'GET':
#         sellers = Seller.objects.all()
#         serializer = SellerSerializer(sellers, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = SellerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)






@api_view()
def seller_single_view(request, pk):
    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)
    


# @api_view(['GET', 'POST'])
# def products_view(request):

#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductDetailSerializer(products, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = ProductCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
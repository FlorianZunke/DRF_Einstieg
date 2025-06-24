from rest_framework import serializers
from market_app.models import Market, Seller, Product

def validate_noX(value):

    errors =[]

    if 'X' in value:
        errors.append('no X in locations')
    if 'Y' in value:
        errors.append('no Y in locations')
    
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_noX])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance


class SellersDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many=True)


class SellersCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError({"messsage": "passt halt nicht mit den IDs"})
        return value

    def create(self, validated_data):
        market_id= validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets_list = Market.objects.filter(id__in=market_id)
        seller.markets.set(markets_list)
        return seller
    


class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.StringRelatedField(many=True)
    seller = serializers.StringRelatedField(many=True)



class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    seller = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        market = Market.objects.filter(id__in=value)
        if len(market) != len(value):
            raise serializers.ValidationError({"messsage": "passt halt nicht mit den IDs"})
        return value

    def validate_sellers(self, value):
        seller = Seller.objects.filter(id_in=value)
        if len(seller) != len(value):
            raise serializers.ValidationError({"messsage": "passt halt nicht mit den IDs"})
        return value


    def create(self, validated_data):
        market_id= validated_data.pop('market')
        seller_id= validated_data.pop('seller')
        product = Product.objects.create(**validated_data)
        markets_list = Market.objects.filter(id__in=market_id)
        sellers_list = Seller.objects.filter(id__in=seller_id)
        product.market.set(markets_list)
        product.seller.set(sellers_list)
        return product

# {
# "name" : "Eis",
# "description" : "was kaltes zum essen",
# "price" : "3.99",
# "market" : [1],
# "seller" : [1]
# }
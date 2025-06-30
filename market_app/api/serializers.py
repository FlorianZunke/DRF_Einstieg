from rest_framework import serializers
from market_app.models import Market, Seller, Product

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

    def validate_name(self, value):
        errors =[]

        if 'X' in value:
            errors.append('no X in locations')
        if 'Y' in value:
            errors.append('no Y in locations')
    
        if errors:
            raise serializers.ValidationError(errors)
        return value


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_id = serializers.PrimaryKeyRelatedField(
        queryset = Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )

    market_count = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        exclude = []

    def get_market_count(self, obj):
        return obj.markets.count()
    


class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = MarketSerializer(write_only=True)
    seller = SellerSerializer(write_only=True)



class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.IntegerField(write_only=True)
    seller = serializers.IntegerField(write_only=True)

    def validate_market(self, value):
        if not Market.objects.filter(id=value).exists():
            raise serializers.ValidationError("Market with this ID does not exist.")
        return value

    def validate_seller(self, value):
        if not Seller.objects.filter(id=value).exists():
            raise serializers.ValidationError("Seller with this ID does not exist.")
        return value

    def create(self, validated_data):
        market_id = validated_data.pop('market')
        seller_id = validated_data.pop('seller')
        market = Market.objects.get(id=market_id)
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.create(market=market, seller=seller, **validated_data)
        return product
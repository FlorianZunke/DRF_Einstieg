from rest_framework import serializers
from market_app.models import Market, Seller, Product

class MarketSerializer(serializers.ModelSerializer):

    sellers = serializers.StringRelatedField(many=True, read_only=True)


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


class MarketHyperlinkSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Market
        fields = ['id', 'url', 'name', 'location', 'description', 'net_worth']


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
    

class SellerListSerializer(SellerSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        fields = ['url', 'name', 'market_id', 'market_count', 'contact_info']
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'







# class ProductDetailSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=50, decimal_places=2)
#     market = MarketSerializer(write_only=True)
#     seller = SellerSerializer(write_only=True)


# class ProductCreateSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=50, decimal_places=2)
#     market = serializers.IntegerField(write_only=True)
#     seller = serializers.IntegerField(write_only=True)

#     def validate_market(self, value):
#         if not Market.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Market with this ID does not exist.")
#         return value

#     def validate_seller(self, value):
#         if not Seller.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Seller with this ID does not exist.")
#         return value

#     def create(self, validated_data):
#         market_id = validated_data.pop('market')
#         seller_id = validated_data.pop('seller')
#         market = Market.objects.get(id=market_id)
#         seller = Seller.objects.get(id=seller_id)
#         product = Product.objects.create(market=market, seller=seller, **validated_data)
#         return product
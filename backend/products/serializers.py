from rest_framework import serializers
from products.models import Product, ProductReview


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            representation['created_by'] = {"username":instance.created_by.username, "email": instance.created_by.email}
        except:
            representation['created_by'] = {"username": "", "email": ""}
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    user_reviews = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        # average of review
        reviews = ProductReview.objects.filter(product=obj)
        total_rating = 0
        if reviews.count() > 0:
            for review in reviews:
                total_rating += review.rating
            return round(total_rating / reviews.count(),2)
        else:
            return 0

    def get_total_reviews(self, obj):
        review_list = list()
        review_list.append({
            "one_star_count", ProductReview.objects.filter(product=obj, rating=1).count(),
        })
        review_list.append({
            "two_star_count", ProductReview.objects.filter(product=obj, rating=2).count(),
        })
        review_list.append({
            "three_star_count", ProductReview.objects.filter(product=obj, rating=3).count(),
        })
        review_list.append({
            "four_star_count", ProductReview.objects.filter(product=obj, rating=4).count(),
        })
        review_list.append({
            "five_star_count", ProductReview.objects.filter(product=obj, rating=5).count(),
        })
        return review_list

    def get_user_reviews(self, obj):
        reviews = ProductReview.objects.filter(product=obj)
        review_list = list()
        for review in reviews:
            review_list.append(
                {
                    "username": review.review_by.username,
                    "comment": review.comment,
                    "rating": review.rating,
                    "date": review.get_date()
                }
            )
        return review_list


    class Meta:
        model = Product
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    review_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ('created_by',)
        extra_kwargs = {
            'product': {'required': True},
            'rating': {'required': True},
            'comment': {'required': True},
        }

    def create(self, validated_data):
        return ProductReview.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def validate(self, data):
        if data['rating'] < 1 or data['rating'] > 5:
            raise serializers.ValidationError("Rating should be between 1 and 5")
        return data

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist")
        return value

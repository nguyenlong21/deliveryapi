from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Delivery, Shipper, Promotion, Order, Tag, User, Comment, OrderComment, Action, Rating

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','created_date']

class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'name', 'image','created_date','category']

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ShipperSerializer(ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Shipper
        fields = ['id', 'name', 'image', 'created_date', 'delivery', 'tag']

class ShipperDetailSerializer(ShipperSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = ShipperSerializer.Meta.model
        fields = ShipperSerializer.Meta.fields +['description', 'tag']

class PromotionSerializer(ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'image', 'created_date', 'delivery']

class PromotionDetailSerializer(ShipperSerializer):
    class Meta:
        model = PromotionSerializer.Meta.model
        fields = PromotionSerializer.Meta.fields +['description']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'name', 'image', 'created_date', 'delivery']

class OrderDetailSerializer(ShipperSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = OrderSerializer.Meta.model
        fields = OrderSerializer.Meta.fields +['description']

class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date']

class OrderCommentSerializer(ModelSerializer):
    class Meta:
        model = OrderComment
        fields = ['id', 'content', 'created_date', 'updated_date']

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'type', 'created_date']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rate', 'created_date']
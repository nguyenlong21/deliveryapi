from typing import Union

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Category, Delivery, Shipper, Promotion, Order, User, Comment, OrderComment, Action, Rating
from .perms import CommentOwnerPermisson
from .serializers import CategorySerializer, DeliverySerializer, ShipperSerializer, PromotionSerializer, \
    OrderSerializer, UserSerializer, ShipperDetailSerializer, PromotionDetailSerializer, OrderDetailSerializer, \
    CommentSerializer, OrderCommentSerializer, ActionSerializer, RatingSerializer

class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q

class DeliveryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Delivery.objects.filter(active=True)
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Get the shipper of delivery',
        responses={
            status.HTTP_200_OK: ShipperSerializer()
        }
    )

    @action(methods=['get'], detail=True, url_path='shippers')
    def get_shippers(self, request, pk):
        shippers = self.get_object().shippers.filter(active=True)
        kw = request.query_params.get('kw')

        if kw is not None:
            shippers = shippers.filter(name__icontains=kw)

        return Response(data=ShipperSerializer(shippers, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='promotions')
    def get_promotions(self, request, pk):
        promotion = self.get_object().promotions.filter(active=True)

        kw = request.query_params.get('kw')
        if kw is not None:
            promotion = promotion.filter(name__icontains=kw)

        return Response(data=PromotionSerializer(promotion, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='orders')
    def get_orders(self, request, pk):
        order = self.get_object().orders.filter(active=True)

        kw = request.query_params.get('kw')
        if kw is not None:
            order = order.filter(name__icontains=kw)

        return Response(data=OrderSerializer(order, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ViewSet,generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

class ShipperViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Shipper.objects.filter(active=True)
    serializer_class = ShipperDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['add_comment', 'take_action', 'rate']:
            return[permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, shipper=self.get_object(), creator=request.user)

            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='like')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type=action_type, creator=request.user, shipper=self.get_object())

            return Response(ActionSerializer(action).data, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rate'])
        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating, creator=request.user, shipper=self.get_object())

            return Response(RatingSerializer(r).data, status=status.HTTP_200_OK)

class PromotionViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Promotion.objects.filter(active=True)
    serializer_class = PromotionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
class OrderViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = OrderComment.objects.create(content=content, order=self.get_object(), creator=request.user)

            return Response(OrderCommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)



def index(request):
    return HttpResponse('Delivery App')




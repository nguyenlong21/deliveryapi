from . import views

from django.urls import path, include

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, 'category')
router.register('deliveries', views.DeliveryViewSet, 'delivery')
router.register('shippers', views.ShipperViewSet, 'shipper')
router.register('promotions', views.PromotionViewSet, 'promotion')
router.register('orders', views.OrderViewSet, 'order')
router.register('users', views.UserViewSet, 'user')
router.register('comments', views.CommentViewSet, 'comment')

urlpatterns = [
    path('', include(router.urls), name="index"),
]
from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')


class ModelBase(models.Model):
    name = models.CharField(max_length=255, null=False)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(ModelBase):

    def __str__(self):
        return self.name


class Delivery(ModelBase):
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='deliverys/%Y/%m')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", 'category')

class Shipper(ModelBase):
    description = RichTextField()
    image = models.ImageField(null=True, blank=True, upload_to='shippers/%Y/%m')
    delivery = models.ForeignKey(Delivery, null=True, related_name='shippers', on_delete=models.SET_NULL)
    tag = models.ManyToManyField('Tag', null=True, blank=True, related_name='shippers')

    def __str__(self):
        return self.name


class Promotion(ModelBase):
    description = RichTextField()
    image = models.ImageField(null=True, blank=True, upload_to='promotions/%Y/%m')
    delivery = models.ForeignKey(Delivery, null=True, related_name='promotions',on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Order(ModelBase):
    description = RichTextField()
    image = models.ImageField(null=True, blank=True, upload_to='orders/%Y/%m')
    delivery = models.ForeignKey(Delivery, null=True, related_name='orders',on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    shipper = models.ForeignKey(Shipper, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class OrderComment(models.Model):
    content = models.TextField()
    order = models.ForeignKey(Order, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class ActionBase(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Action(ActionBase):
    LIKE, DISLIKE, LOVE = range(3)
    ACTIONS = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
        (LOVE, 'Love')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)

class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)

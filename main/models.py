from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

class Banner(models.Model):
    image = models.ImageField(upload_to="brand_images/")
    alt_text = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = '1. Banners'

    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cat_images/")

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural = '2. Categories'

    def __str__(self):
        return self.title
    
class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_images/")

    class Meta:
        verbose_name_plural = '3. Brands'

    def __str__(self):
        return self.title
    
class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def color_tag(self):
        return mark_safe('<div style="width:25px; height:25px; background-color:%s"></div>' % (self.color_code))

    class Meta:
        verbose_name_plural = '4. Colors'

    def __str__(self):
        return self.title
    
class Size(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '5. Sizes'

    def __str__(self):
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=400)
    detail = models.TextField()
    specification = models.TextField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '6. Products'

    def __str__(self):
        return self.title
    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="product_images/", null=True)

    class Meta:
        verbose_name_plural = '7. ProductAttributes'

    def __str__(self):
        return self.product.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

status_choice=(
    ('process', 'In Process'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=status_choice, default='process', max_length=150)

    class Meta:
        verbose_name_plural = '8. Orders'

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

RATING = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.CharField(choices=RATING, max_length=150)

    class Meta:
        verbose_name_plural = 'Reviews'

    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wishlist'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50, null=True)
    address = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
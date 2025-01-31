from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered', 'Delivered'),
)
MODES = (
    ('COD', 'COD'),
    ('Debit/Credit Card','Debit/Credit Card'),
    ('UPI','UPI'),
)
PAY_STATUS = (
    
    ('Paid','Paid'),
    ('Pending','Pending')
)
CITIES = (('Nagpur','Nagpur'),
              ('Pune','Pune'),
              ('Nashik','Nashik'),
              ('Aurangabad','Aurangabad'),
              ('Wardha','Wardha'))


# to replace the default __str__ return function for User
def get_first_name(self):
    return f'{self.first_name} {self.last_name}'

# returns first name and last name for the user
User.add_to_class("__str__", get_first_name)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug from the name field if it's not set
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300,default=None)
    desc = models.TextField()
    brand = models.CharField(max_length=30,default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', default=None)
    category = models.ManyToManyField(Category)
    slug_field = models.SlugField(max_length=300,null=True,blank=True)

    def __str__(self) -> str:
        return str(f'[{self.pk}] {self.name[:15]}')
    
    def save(self,*args,**kwargs):
        self.slug_field = slugify(self.name +'-'+ str(self.pk))
        super(Product, self).save(*args,**kwargs)

    def getBrand(self):
        return self.brand
    
    def get_absolute_url(self):
        return self.slug_field

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    plot_no = models.TextField(default=None)
    streetaddr = models.TextField()
    city = models.CharField(max_length=20, default=None)
    pincode = models.PositiveIntegerField()
    
    def _str__(self):
        return str(f'{self.user}')
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None,)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    quantity = models.PositiveIntegerField(default=None)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    details = models.TextField(default=None,blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(f'Order by ,{self.user.username}')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    order = models.ManyToManyField(OrderItem)
    delivery_address = models.CharField(max_length=300, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20,choices=MODES, default=None)
    payment_status = models.CharField(max_length=20,choices=PAY_STATUS, default='Pending')
    order_status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')
    def __str__(self):
        return str(f'{self.user.first_name} {self.user.last_name} : payment {self.payment_status}')

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=MODES)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=PAY_STATUS)

    def __str__(self):
        return f"Payment for Order #{self.pk} is {self.payment_status} via {self.payment_method}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return str(f'{self.rating} rating by {self.user.username} for {self.product.name}')
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(f"{self.pk} {self.user.first_name}'s Cart: {self.product.name}")
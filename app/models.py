from typing import Counter, NoReturn
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import tree
from django.utils.timezone import now
STATE_CHOICE=(
   ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
   ("Andhra Pradesh","Andhra Pradesh"),
   ("Arunachal Pradesh","Arunachal Pradesh"),
   ("Assam","Assam"),
   ("Bihar","Bihar"),
   ("Chhattisgarh","Chhattisgarh"),
   ("Chandigarh","Chandigarh"),
   ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
   ("Daman and Diu","Daman and Diu"),
   ("Delhi","Delhi"),
   ("Goa","Goa"),
   ("Gujarat","Gujarat"),
   ("Haryana","Haryana"),
   ("Himachal Pradesh","Himachal Pradesh"),
   ("Jammu and Kashmir","Jammu and Kashmir"),
   ("Jharkhand","Jharkhand"),
   ("Karnataka","Karnataka"),
   ("Kerala","Kerala"),
   ("Ladakh","Ladakh"),
   ("Lakshadweep","Lakshadweep"),
   ("Madhya Pradesh","Madhya Pradesh"),
   ("Maharashtra","Maharashtra"),
   ("Manipur","Manipur"),
   ("Meghalaya","Meghalaya"),
   ("Mizoram","Mizoram"),
   ("Nagaland","Nagaland"),
   ("Odisha","Odisha"),
   ("Punjab","Punjab"),
   ("Pondicherry","Pondicherry"),
   ("Rajasthan","Rajasthan"),
   ("Sikkim","Sikkim"),
   ("Tamil Nadu","Tamil Nadu"),
   ("Telangana","Telangana"),
   ("Tripura","Tripura"),
   ("Uttar Pradesh","Uttar Pradesh"),
   ("Uttarakhand","Uttarakhand"),
   ("West Bengal","West Bengal")
)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length=50)
    profile_pic=models.ImageField(upload_to='profileimg',default="profile1.png", null=True, blank=True)

def __str__(self):
    return str(self.id)








CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    timestamp=models.DateTimeField(default=now)

    product_image=models.ImageField(upload_to='productimg',default="product.png")
 
    product_image_child1=models.ImageField(upload_to='productimg_child',default="productchild1.png", null=True, blank=True)
    
    product_image_child2=models.ImageField(upload_to='productimg_child',default="productchild2.png", null=True, blank=True)

    product_image_child3=models.ImageField(upload_to='productimg_child',default="productchild3.png", null=True, blank=True)


    def __str__(self):
        return str(self.id)
# Ratings stuff starts 
    def get_rating(self):
        total=sum(int(review['rate'])  for review in self.reviews.values())
        #count=count( int(c['comment'])  for c in self.reviews.values()) 
        try:
            td=total/self.reviews.count()
        except ZeroDivisionError:
            td=0    
        return td

    def count_rating5(self):
        count5=0
        for review in self.reviews.values():
            if review['rate']==5:
                count5=count5+1
        return count5  
   
    def count_rating4(self):
        count4=0
        for review in self.reviews.values():
            if review['rate']==4:
                count4=count4+1
        return count4     

    def count_rating3(self):
        count3=0
        for review in self.reviews.values():
            if review['rate']==3:
                count3=count3+1
        return count3  

    def count_rating2(self):
        count2=0
        for review in self.reviews.values():
            if review['rate']==2:
                count2=count2+1
        return count2 

    def count_rating1(self):
      count1=0
      for review in self.reviews.values():
        if review['rate']==1:
            count1=count1+1
        return count1     




class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price    

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
) 

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price 

    @property
    def user_quantity(self):
        return self.quantity 

class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    time_st=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()   

class ProductComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, related_name='reviews' , on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    #customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)
    rate=models.IntegerField(default=5)
    

    def __str__(self):
        return self.comment[0:50] + "...." + "by.." + self.user.username
    
    def get_comment_count(self):
        return self.comment.count




# Create your models here.
#,default="profile1.png", null=True, blank=True
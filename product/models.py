from django.db import models

# Create your models here.

class Department(models.Model):
    d_name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    def __str__(self):
        return self.d_name

class Branch(models.Model):
    b_name = models.CharField(max_length=30)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.b_name

class Category(models.Model):
    c_name = models.CharField(max_length=30)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    def __str__(self):
        return  self.c_name + " - " + self.branch.b_name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    p_name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    img = models.ImageField(upload_to='photos/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.p_name
    class Meta:
        ordering = ['created']

class Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='photos/%Y/%m/%d/')
    def __str__(self):
        return self.product.p_name +" ( "+ str(self.id) +" )"
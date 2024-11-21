from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Category Image")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Parent Category"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    @property
    def is_parent(self):
        return self.parent is None


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Tag Name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name="Product Image", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(verbose_name="Stock Quantity")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        verbose_name="Category"
    )
    tags = models.ManyToManyField('Tag', through='ProductTag', related_name='products', verbose_name="Tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0
    

class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_tags", verbose_name="Product")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="product_tags", verbose_name="Tag")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added On")

    class Meta:
        verbose_name = "Product-Tag Relation"
        verbose_name_plural = "Product-Tag Relations"
        unique_together = ('product', 'tag') 

    def __str__(self):
        return f"{self.product.name} - {self.tag.name}"



from django.db import models
from django.db.models import Sum, F


class Cart(models.Model):
    STATUS = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='cart', 
        verbose_name="User"
    )
    status = models.CharField(max_length=10, choices=STATUS, default = "open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.name or self.user.email} cart"
    
    @property
    def get_cart_total(self):
        """
        Calculate the total value of all items in the user's cart.
        """
        total = CartItem.objects.filter(cart__user=self.user, cart__id=self.id).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total']
        return float(total) or 0.0 
    

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='cart_items', 
        verbose_name="Cart"
    )
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE, 
        related_name='cart_items', 
        verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together: list[str] = ['cart', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.cart} items"
    
    @property
    def get_total(self):
        return self.quantity * self.product.price

    

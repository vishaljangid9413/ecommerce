from django.test import TestCase
from accounts.models import User
from products.models import Product, Category
from cart.models import Cart, CartItem

class CartModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            name="John Doe",
            mobile=1234567888,
            email="johndoe@example.com",
            password="testpassword"
        )

        # Create a category
        self.category = Category.objects.create(name="Electronics")

        # Create a product
        self.product = Product.objects.create(
            name="Smartphone",
            description="A new smartphone",
            price=599.99,
            stock=10,
            category=self.category
        )

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

        # Add a cart item
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.status, "open")
        self.assertEqual(str(self.cart), f"{self.user.name} cart")

    def test_cart_total_property(self):
        # Check the total value of the cart
        self.assertAlmostEqual(self.cart.get_cart_total, 1199.98)

        # Add another item to the cart
        another_product = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop",
            price=999.99,
            stock=5,
            category=self.category
        )
        CartItem.objects.create(cart=self.cart, product=another_product, quantity=1)

        # Check the updated cart total
        self.assertAlmostEqual(self.cart.get_cart_total, 2199.97)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(str(self.cart_item), f"{self.cart} items")

    def test_cart_item_total_property(self):
        # Check the total value of the cart item
        self.assertAlmostEqual(self.cart_item.get_total, 1199.98)

        # Update the quantity
        self.cart_item.quantity = 1
        self.cart_item.save()

        # Check the updated total value
        self.assertAlmostEqual(self.cart_item.get_total, 599.99)

    def test_cart_item_unique_constraint(self):
        # Attempt to create a duplicate cart item
        with self.assertRaises(Exception):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

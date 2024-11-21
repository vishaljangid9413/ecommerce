from django.test import TestCase
from .models import Category, Tag, Product, ProductTag


class CategoryModelTest(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Electronics")
        self.child_category = Category.objects.create(name="Mobile Phones", parent=self.parent_category)

    def test_category_creation(self):
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertEqual(self.child_category.name, "Mobile Phones")

    def test_category_parent_relationship(self):
        self.assertTrue(self.child_category.parent)
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_category_is_parent_property(self):
        self.assertTrue(self.parent_category.is_parent)
        self.assertFalse(self.child_category.is_parent)

    def test_category_string_representation(self):
        self.assertEqual(str(self.parent_category), "Electronics")
        self.assertEqual(str(self.child_category), "Mobile Phones")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Laptops")
        self.product = Product.objects.create(
            name="Dell Inspiron",
            description="A powerful laptop.",
            price=599.99,
            stock=10,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Dell Inspiron")
        self.assertEqual(self.product.description, "A powerful laptop.")
        self.assertEqual(self.product.price, 599.99)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.category, self.category)

    def test_product_is_in_stock_property(self):
        self.assertTrue(self.product.is_in_stock)

        # Update stock to zero
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), "Dell Inspiron")


class ProductTagModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tablets")
        self.product = Product.objects.create(
            name="iPad Pro",
            description="Apple tablet",
            price=799.99,
            stock=5,
            category=self.category
        )
        self.tag = Tag.objects.create(name="Apple")
        self.product_tag = ProductTag.objects.create(product=self.product, tag=self.tag)

    def test_product_tag_creation(self):
        self.assertEqual(self.product_tag.product, self.product)
        self.assertEqual(self.product_tag.tag, self.tag)

    def test_product_tag_relationship(self):
        self.assertIn(self.product_tag, ProductTag.objects.all())
        self.assertIn(self.product, self.tag.products.all())
        self.assertIn(self.tag, self.product.tags.all())

    def test_product_tag_string_representation(self):
        self.assertEqual(str(self.product_tag), "iPad Pro - Apple")

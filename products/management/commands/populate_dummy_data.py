import random
from django.core.management.base import BaseCommand
from products.models import Category, Tag, Product, ProductTag

class Command(BaseCommand):
    help = "Populate the database with valid dummy data for testing purposes."

    def handle(self, *args, **kwargs):
        categories_data = [
            "Electronics", "Clothing", "Home Appliances", "Books", "Sports"
        ]
        subcategories_data = {
            "Electronics": ["Mobiles", "Laptops", "Cameras"],
            "Clothing": ["Men", "Women", "Kids"],
            "Home Appliances": ["Kitchen", "Cleaning", "Cooling"],
            "Books": ["Fiction", "Non-fiction", "Educational"],
            "Sports": ["Cricket", "Football", "Gym Equipment"]
        }
        tags_data = [
            "New Arrival", "Best Seller", "Discounted", "Premium Quality", "Limited Edition"
        ]
        products_data = [
            {"name": "Smartphone", "price": 199.99, "stock": 50, "description": "A powerful smartphone with cutting-edge features."},
            {"name": "Laptop", "price": 899.99, "stock": 20, "description": "Lightweight and high-performance laptop."},
            {"name": "Washing Machine", "price": 499.99, "stock": 15, "description": "Energy-efficient washing machine."},
            {"name": "T-Shirt", "price": 19.99, "stock": 200, "description": "Comfortable and stylish cotton T-shirt."},
            {"name": "Cricket Bat", "price": 39.99, "stock": 80, "description": "Professional cricket bat for players."},
            {"name": "Novel", "price": 14.99, "stock": 100, "description": "A gripping fiction novel to keep you hooked."}
        ]

        # Create categories and subcategories
        print("Creating categories and subcategories...")
        categories = {}
        for category_name in categories_data:
            category = Category.objects.create(name=category_name)
            categories[category_name] = category
            for subcategory_name in subcategories_data[category_name]:
                Category.objects.create(name=subcategory_name, parent=category)
        print("Categories and subcategories created.")

        # Create tags
        print("Creating tags...")
        tags = [Tag.objects.create(name=tag_name) for tag_name in tags_data]
        print("Tags created.")

        # Create products
        print("Creating products...")
        products = []
        for product_data in products_data:
            category = random.choice(list(categories.values()))  
            product = Product.objects.create(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                stock=product_data["stock"],
                category=category
            )
            products.append(product)
        print("Products created.")

        # Assign tags to products
        print("Assigning tags to products...")
        for product in products:
            assigned_tags = random.sample(tags, random.randint(1, 3)) 
            for tag in assigned_tags:
                ProductTag.objects.create(product=product, tag=tag)
        print("Tags assigned to products.")

        print(self.style.SUCCESS("Valid dummy data populated successfully!"))

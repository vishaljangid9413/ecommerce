from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Category Name',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'parent': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'name': 'Category Name',
            'image': 'Category Image',
            'parent': 'Parent Category',
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock', 'category', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Description',
                'rows': 4,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Price',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Stock Quantity',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Product Description',
            'image': 'Product Image',
            'price': 'Price',
            'stock': 'Stock Quantity',
            'category': 'Category',
            'tags': 'Tags',
        }

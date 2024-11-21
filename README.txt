
# E-commerce Web Application

## Description

This project is a fully functional e-commerce web application built with Django. It includes features like user authentication, product catalog, cart functionality, categories, tags, and much more. The app allows users to register, add products to their cart, view their cart, checkout, and more.

---

## Table of Contents

1. [Project Setup](#setup)
2. [Running the Application](#run)
3. [Features](#features)
4. [Running Tests](#tests)
5. [Custom Commands](#custom-commands)
6. [Troubleshooting](#troubleshooting)

---

## Setup

Follow the steps below to set up the project from scratch.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/project-name.git
cd project-name
```

### 2. Create a Virtual Environment

A virtual environment helps isolate your project dependencies from the system-wide Python packages. You can create one by following these steps:

```
# For Setup virtual environment
pip install pipenv
```

### 3. Activate the Virtual Environment

Activate the virtual environment by running the following commands:

```bash
pipenv shell

```

Once the environment is activated, your terminal prompt should change to indicate that you're now working inside the virtual environment.

### 4. Install Project Dependencies

Install the required dependencies from `requirements.txt` using pip:

```bash
pipenv install
```

### 5. Set Up Environment Variables

Make sure to create a `.env` file in the root directory to store sensitive information such as your secret key, database credentials, etc. You can copy from `.env.example` if provided.

```env
PROJECT_KEY='your project secret key'
ENV_EMAIL_HOST_USER='your google certified email'
ENV_EMAIL_HOST_PASSWORD='your email app password' 
```

---

## Database Setup

### 1. Run Migrations

Run the migrations to set up your database schema:

```bash
python manage.py migrate
```

This will create the necessary database tables for all your models.

### 2. Create a Superuser

To access the Django admin panel, you need to create a superuser account. Run the following command:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter a username, email, and password.

### 3. Run the Development Server

Now, you can run the development server:

```bash
python manage.py runserver
```

Your site will be accessible at `http://127.0.0.1:8000/`.

---

## Custom Commands

The project includes a custom command to populate the database with dummy data. This is helpful when you need sample data for testing or development.

### 1. Run the Custom Command

To fill your database with dummy data, run the following command:

```bash
python manage.py fill_dummy_data
```

This will populate your `Category`, `Tag`, `Product`, and `Cart` models with sample data.

---

## Features

1. **User Authentication**
   - Register new users
   - Login and logout functionality
   - Admin panel for managing users and content

2. **Product Catalog**
   - Browse products by category
   - View product details

3. **Shopping Cart**
   - Add products to cart
   - Update quantity of products
   - Remove items from the cart
   - View total price of items in the cart

4. **Categories & Tags**
   - Categorize products into various categories
   - Tag products with different tags for better searching

5. **Order Management (Optional)**
   - Checkout and place an order

6. **User Management (Optional)**
   - See all the register users (except superusers)
   - Activate/Deactivate and can delete a user
 
7. **Profile**
   - Explore your own profile

---

## Running Tests

To ensure that everything works as expected, you can run the test cases.

### 1. Run All Tests

Django provides a built-in test runner. You can use it to run all tests:

```bash
python manage.py test
```

This will automatically discover and run all tests in your project. If you want to run tests for a specific app, you can specify the app name:

```bash
python manage.py test cart
```

### 2. Test Coverage

Ensure all models and functionalities are tested by adding more tests in the `tests.py` files of each app. Test cases should cover validation, creation, and updating of records.

---

## Navigating the Site

1. **Homepage**: After logging in or as a guest, you will land on the homepage where you can browse product categories and view featured products.
2. **Product Page**: Click on any product to view its details, such as name, description, and price.
3. **Add to Cart**: You can add products to your cart, adjust their quantities, and remove items from the cart.
4. **Checkout**: Proceed to the checkout page to finalize your order (if order management is implemented).
5. **Admin Panel**: Access the Django admin panel at `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

---

## Troubleshooting

Here are a few common issues you might encounter and their solutions:

1. **"ModuleNotFoundError"**: Ensure all dependencies are installed by running `pip install -r requirements.txt`.

2. **"FileNotFoundError" for Images**: Ensure that your static files and media files are properly configured in `settings.py`. You may need to set `MEDIA_URL` and `MEDIA_ROOT`.

---

## Conclusion

This e-commerce project allows you to build a robust online store with features such as user authentication, product management, and cart functionality. With a fully functional admin panel and the ability to populate data with custom commands, this project is highly extensible and can serve as a foundation for further development.

---

### Notes:

- **Make sure to keep your environment variables secure** (e.g., `SECRET_KEY`, `EMAIL`, `APP_PASSWORD`).
- **Consider using Docker** for a more consistent development environment across machines.

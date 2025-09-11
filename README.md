# University Bookstore API - COMS4153 Cloud Computing Homework 1
Di Wang (Columbia University)

A simple FastAPI microservice for managing a university bookstore's products and categories. This project demonstrates basic REST API design.

## Project Overview

This microservice provides a RESTful API for managing:
- **Categories**: Product categories (e.g., Apparel, Drinkware, Accessories)
- **Products**: Individual bookstore items with detailed inventory information

## API Endpoints

### Categories
- `POST /categories` - Create a new category
- `GET /categories` - List all categories
- `GET /categories/{category_id}` - Get a specific category
- `PUT /categories/{category_id}` - Update a category
- `DELETE /categories/{category_id}` - Delete a category

### Products
- `POST /products` - Create a new product
- `GET /products` - List all products
- `GET /products/{product_id}` - Get a specific product
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product

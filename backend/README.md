# Backend

This directory contains the backend code for the ShopWise platform, including RESTful APIs and business logic.

## Contents

### API Endpoints: Implementation of RESTful API endpoints.

- `api/products/`:

  Contains the implementation of the **_products_** endpoint, which allows users to retrieve product data and recommendations.

- `api/products/search/`:

  Contains the implementation of the **_search_** endpoint, which allows users to search for products based on their name.

- `api/products/categories/`:

  Contains the implementation of the **_categories_** endpoint, which allows users to retrieve all product categories.

- `api/products/compare/`:

  Contains the implementation of the **_compare_** endpoint, which allows users to compare the same product across different stores.

- `api/products/recommendations/<int:pk>/`:

  Contains the implementation of the **_recommendations_** endpoint, which allows users to retrieve product recommendations based on their wishlist/grocery_list.

- `api/wishlist/<int:pk>/`:

  Contains the implementation of the **_wishlist_** endpoint, which allows users to add and remove products from their wishlist.

- `api/retailers/`:

  Contains the implementation of the **_retailers_** endpoint, which allows users to retrieve retailer data.

- `api/retailers/<int:pk>/products/`:

  Contains the implementation of the **_retailer_products_** endpoint, which allows users to retrieve products from a specific retailer.

- `auth/register/`:

  Contains the implementation of the **_register_** endpoint, which allows users to register on the platform.

- `auth/login/`:

  Contains the implementation of the **_login_** endpoint, which allows users to login to the platform.

- `auth/token/refresh/`:

  Contains the implementation of the **_refresh_token_** endpoint, which allows users to refresh their access token.

- `auth/profile/`:

  Contains the implementation of the **_profile_** endpoint, which allows users to retrieve and update their profile data.

### Business Logic: handling Product data, Users, and Recommendations.

### Database Models: Models for interacting with the database.

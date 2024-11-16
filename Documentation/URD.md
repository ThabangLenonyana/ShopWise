# User Requirements Document (URD)

**Project Title: ShopWise - Product Comaparison & Recommendation Platform**

**Document Version : 1.0**

**Prepared by: Jian Yang Administration**

**Date: 16/11/2024**

## 1. Introduction

### 1.1 Purpose

This document outlines the user requirements for a Product Comparison and Recommendation Platform that allows users to:

- Browse and select products from different stores.

- Compare product prices across stores.

- Receive personalized product recommendations based on their preferences and browsing history.

The platform integrates **Web Scraping, RESTful APIs, Azure cloud services, and Machine Learning algorithms** to collect and process product data, manage user interactions, and deliver recommendations.

### 1.2 Scope

1. Scrape product and pricing data from multiple online stores.
2. Expose RESTful APIs to fetch product categories, store information, product comparisons and recommendations.
3. Provide users with personalized product recommendations using machine learning.
4. Implement logging, monitoring, and performance tracking using Azure services such as Prometheus and Application Insights.

## 2. System Overview

### 2.1 Funcional Overview

The Product Comparison and Recommendation Platform will consist of the following key components:

1. **Web Scraping Module:** Collects product data from external websites (e.g., pricing, availability).

2. **Backend (API Layer):** Exposes RESTful APIs to handle requests from the frontend and serve data such as product listings, price comparisons, and recommendations.

3. **Frontend (UI Layer):** The user interface where users can browse categories, view product prices across stores, and receive recommendations.

4. **Machine Learning Pipeline:** Analyzes user behavior and product attributes to generate personalized recommendations.

5. **Cloud Integration:** Use Azure services for hosting the system, including databases, APIs, and monitoring.

## 3. System Architecture

### 3.1 High-Level Architecture Diagram

![High-Level Architecture](Diagrams/High%20Level%20Architecture.svg)

### 3.2 Key Compenents

| **Component**                          | **Function**                                                                                              | **Technology**                                                                                                                                   | **Additional Details**                                                                                                                                                                                       |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Web Scraping Module**                | Scrapes product data (name, price, availability) from multiple online stores.                             | - Scrapy or Puppeteer for scraping<br>- Azure Functions for scheduling and running scraping tasks                                                | - Data Storage: Azure SQL Database or Cosmos DB<br>- Frequency: Periodic (e.g., daily or weekly)                                                                                                             |
| **Backend (API Layer)**                | Provides RESTful APIs for frontend interactions (product listings, price comparisons, recommendations).   | - Python (Django Rest Framework)                                                                                                                 | - Endpoints: <br> • `GET /categories` <br> • `GET /products` <br> • `GET /product` <br> • `POST /compare-prices` <br> • `GET /recommendations`<br>- Security: OAuth 2.0 or JWT for authentication            |
| **Frontend (UI Layer)**                | User interface for browsing product categories, viewing price comparisons, and receiving recommendations. | - React (web) or React Native (mobile)                                                                                                           | - Components: <br> • Product category browsing & filtering <br> • Price comparison display <br> • Recommendation display <br> • User authentication & profile management <br> - API Integration with backend |
| **Machine Learning Pipeline**          | Provides personalized recommendations based on user interactions (viewed products, previous purchases).   | - Azure Machine Learning Service or Databricks for model training and deployment<br>- Python for model building                                  | - Recommendation Logic: <br> • Collaborative Filtering (user behavior)<br> • Content-Based Filtering (product attributes)                                                                                    |
| **Cloud Integration (Azure Services)** | Hosts platform infrastructure, databases, APIs, and monitoring tools on Azure.                            | - Azure SQL Database or Cosmos DB<br>- Azure API Management<br>- Azure Functions<br>- Azure Monitor & Prometheus<br>- Azure Application Insights | - Services:<br>• Data Storage: Product, store, user data<br>• API Security & Management<br>• Performance monitoring & tracking                                                                               |

## **4. Functional Requirements**

### **4.1 Web Scraping**

- **Frequency**: The system must scrape product data from external websites on a regular basis (daily, weekly, etc.).
- **Data to Extract**:
  - Product Name
  - Price
  - Availability
  - Store Information (e.g., name, URL)
  - Product Specifications (e.g., size, color, brand)
- **Data Storage**: Scraped data must be stored in a structured format in either Azure SQL Database or Cosmos DB.

### **4.2 RESTful API**

The system must expose the following RESTful API endpoints:

1. **`GET /categories`**: Fetch a list of product categories.
2. **`GET /products`**: Fetch products within a selected category, with optional filters for price range.
3. **`GET /product`**: Fetch detailed information for a specific product.
4. **`POST /compare-prices`**: Compare prices for a selected product across multiple stores.
5. **`GET /recommendations`**: Fetch personalized product recommendations for the user.

### **4.3 Frontend (UI)**

- **User Features**: The UI must enable users to:
  - Browse and filter products by category.
  - View product details, including pricing, availability, and store information.
  - Compare prices of a selected product across multiple stores.
  - View personalized recommendations based on their browsing history or preferences.

### **4.4 Machine Learning Pipeline**

- **Recommendation Methods**:
  - **Collaborative Filtering**: Based on user behavior, such as previously viewed or purchased products.
  - **Content-Based Filtering**: Based on product attributes like category, price, and brand.
- **Deployment**: The machine learning model must be deployed on Azure Machine Learning.
- **Real-Time Recommendations**: The model should provide real-time recommendations through the API.

### **4.5 Logging, Monitoring, and Alerts**

- **Monitoring Tools**:
  - **Prometheus**: Monitor backend services, APIs, and containers. Track metrics such as response times, request counts, and error rates.
  - **Azure Monitor & Application Insights**: Monitor the application, log errors, and provide real-time performance metrics.
- **Alerts**: Set up alerts for:
  - High response times or API failures.
  - Scraping job failures.
  - Unusual user activity patterns.

## **5. Non-Functional Requirements**

### **5.1 Scalability**

- The system must be scalable to handle an increasing number of products, users, and requests.
- The web scraping module must be able to scale and handle scraping from multiple websites concurrently.

### **5.2 Availability**

- The platform should be highly available with minimal downtime. Azure services like App Service or AKS should ensure high availability and redundancy.

### **5.3 Security**

- All APIs must be secured using OAuth 2.0 or JWT to protect user data.
- User credentials should be securely stored, using best practices for password hashing and storage.

### **5.4 Performance**

- The system should be responsive with low latency, especially for product lookups, price comparisons, and recommendations.
- Scraping jobs should not overload the system or cause delays in response times.

### **5.5 Usability**

- The frontend should be user-friendly, intuitive, and responsive across devices (mobile, tablet, and desktop).

## 6. Conclusion

This User Requirements Document (URD) provides a comprehensive overview of the requirements for the Product Comparison and Recommendation Platform. By combining web scraping, RESTful APIs, machine learning, and Azure cloud services, the platform aims to provide users with an efficient and personalized product browsing and purchasing experience.

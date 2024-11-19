import scrapy
from scrapy import Spider, Request
from datetime import datetime
from urllib.parse import urlparse
from myproject.utils.data_cleaner import DataCleaner

class GrocerySpider(Spider):
    name = 'grocery_spider'
    
    # Store selectors for different retailers
    SELECTORS = {
        'shoprite': {
            'product_name': 'h1.pdp__name::text',
            'price': ['div.special-price__price span.now::text', 'div.special-price__price span.before::text'],
            'image_url': 'div.pdp__image__content img::attr(src)',
            'product_url': 'h3.item-product__name a::attr(href)',
            'product_description': ['div.pdp__tabs__tab::text', 'div.pdp__tabs__tab p::text'],
            'pagination': 'div.col-xs-12.col-sm-6.col-md-7 a::attr(href)',
            'product_container': 'div.item-product'
        },
        'checkers': {
            'product_name': 'h1.pdp__name::text',
            'price':  ['div.special-price__price span.now::text', 'div.special-price__price span.before::text'],
            'image_url': 'div.pdp__image__content img::attr(src)',
            'product_url': 'div.item-product__image.__image a::attr(href)',
            'product_description': ['div.pdp__tabs__tab::text', 'div.pdp__tabs__tab p::text'],
            'pagination': 'div.col-xs-12.col-sm-6.col-md-7 a::attr(href)',
            'product_container': 'div.item-product'
        },
        # 'clicks': {
        #     'product_name': 'h1.product-name::text',
        #     'price': ['div.price.blue.typo-h2::text', 'div.price.typo-h2::text'],
        #     'image_url': 'img#imageLink.productImagePrimaryLink::attr(href)',
        #     'product_url': 'div.clickfunct_plp a::attr(href)',
        #     'product_description': 'div.product-desc p::text',
        #     'pagination': 'div.pagination a::attr(href)',
        #     'product_container': 'div.productBlock',
        #     'category': 'ul#breadcrumb.breadcrumb li:not(:first-child):not(:last-child) a::text'
        # },
    }
    
    # Store start URLs for each retailer
    START_URLS = {
        'shoprite': 'https://www.shoprite.co.za/c-2256/All-Departments',
        'checkers': 'https://www.checkers.co.za/c-2256/All-Departments',
        # 'clicks': 'https://www.clicks.co.za/all-brands',
    }
    
    def __init__(self, *args, **kwargs):
        super(GrocerySpider, self).__init__(*args, **kwargs)
        self.visited_urls = set()  # Keep track of visited URLs

    def start_requests(self):
        for retailer, url in self.START_URLS.items():
            yield Request(
                url=url,
                callback=self.parse,
                meta={'retailer': retailer}
            )

    def parse(self, response):
        """
        Main parsing method to handle category pages and extract product links.
        """
        retailer = response.meta['retailer']
        selectors = self.SELECTORS[retailer]

        # Extract and follow product links
        for product in response.css(selectors['product_container']):
            product_url = product.css(selectors['product_url']).get()
            if product_url:
                # Handle relative URLs
                product_url = response.urljoin(product_url)
                
                # Check if the product link has been visited before
                if product_url not in self.visited_urls:
                    self.visited_urls.add(product_url)  # Mark it as visited
                    yield Request(
                        url=product_url,
                        callback=self.parse_product_page,
                        meta={'retailer': retailer},
                        dont_filter=True  # Ensure this request is not filtered
                    )

        # Follow pagination if it exists
        pagination_links = response.css(selectors['pagination']).getall()
        for link in pagination_links:
            next_page = response.urljoin(link)  # Ensure relative links are joined correctly
            
            # Check if the pagination link has been visited before
            if next_page not in self.visited_urls:
                self.visited_urls.add(next_page)  # Mark it as visited
                yield Request(
                    url=next_page,
                    callback=self.parse,
                    meta={'retailer': retailer},
                    dont_filter=True  # Ensure this request is not filtered
                )

    def parse_product_page(self, response: scrapy.http.Response):
        retailer = response.meta['retailer']
        selectors = self.SELECTORS[retailer]
        
        # Extract category based on retailer
        if retailer == 'clicks':
            categories = response.css(selectors['category']).getall()
            category = self.extract_main_category(categories)
            product_name = self.extract_data(response, selectors['product_name'])
        else:
            category = self.extract_category_from_url(response.url)
            product_name = self.extract_data(response, selectors['product_name'])

        # Get raw data
        raw_data = {
            'retailer': retailer,
            'scrape_date': datetime.now().isoformat(),
            'product_name': product_name,
            'price': self.extract_data(response, selectors['price']),
            'image_url': self.extract_data(response, selectors['image_url']),
            'product_url': response.url,
            'category': category,
            'product_description': self.extract_data(response, selectors['product_description']),
        }

        # Clean data using DataCleaner
        cleaned_data = {
            'retailer': raw_data['retailer'],
            'scrape_date': raw_data['scrape_date'],
            'product_name': DataCleaner.clean_text(raw_data['product_name']),
            'price': DataCleaner.clean_price(raw_data['price']),
            'image_url': DataCleaner.clean_url(raw_data['image_url']),
            'product_url': DataCleaner.clean_url(raw_data['product_url']),
            'category': DataCleaner.clean_category(raw_data['category']),
            'product_description': DataCleaner.clean_text(raw_data['product_description'])
        }
        
        yield cleaned_data

    def extract_main_category(self, categories):
        """Extract main category from breadcrumb list"""
        if not categories:
            return "Unknown"
            
        # Filter out empty or None values
        categories = [cat.strip() for cat in categories if cat and cat.strip()]
        
        # Return the second item if available (skip "Home")
        if len(categories) > 1:
            return categories[1]
            
        return categories[0] if categories else "Unknown"

    @staticmethod
    def extract_data(product: scrapy.selector.Selector, selectors: list) -> str:
        """Extract and clean data using a list of selectors"""
        data = []
        if isinstance(selectors, list):
            for selector in selectors:
                extracted = product.css(selector).get()
                if extracted:
                    data.append(extracted.strip())
        else:
            extracted = product.css(selectors).get()
            if extracted:
                data.append(extracted.strip())
        return ' '.join(data) if data else None

    @staticmethod
    def extract_category_from_url(url: str) -> str:
        """Extract category from the URL"""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        if len(path_parts) > 3:
            category = path_parts[2]
            return DataCleaner.clean_category(category)
        return 'Unknown'
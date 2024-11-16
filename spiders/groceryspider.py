import scrapy
from scrapy import Spider, Request
from datetime import datetime
from urllib.parse import urlparse

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
        },
    }
    
    # Store start URLs for each retailer
    START_URLS = {
        'shoprite': 'https://www.shoprite.co.za/c-2256/All-Departments',
    }
    
    def start_requests(self):
        """Initialize requests for each retailer"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        for retailer, url in self.START_URLS.items():
            yield Request(
                url=url,
                callback=self.parse,
                headers=headers,
                meta={'retailer': retailer}
            )
    
    def parse(self, response: scrapy.http.Response):
        retailer = response.meta['retailer']
        selectors = self.SELECTORS[retailer]
        
        # Extract products from the page
        for product in response.css('div.item-product'):
            product_url = self.extract_data(product, selectors['product_url'])
            if product_url:
                product_url = response.urljoin(product_url)
                yield response.follow(
                    product_url,
                    self.parse_product_page,
                    meta={'retailer': retailer},
                    headers=response.request.headers  # Pass headers to the next request
                )
        
        # Follow pagination
        next_page = response.css('div.col-xs-12.col-sm-6.col-md-7 a::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, self.parse, meta={'retailer': retailer}, headers=response.request.headers)
    
    def parse_product_page(self, response: scrapy.http.Response):
        if response.status == 403:
            self.logger.warning(f"Access denied to {response.url}")
            return
        
        retailer = response.meta['retailer']
        selectors = self.SELECTORS[retailer]
        
        yield {
            'retailer': retailer,
            'scrape_date': datetime.now().isoformat(),
            'product_name': self.extract_data(response, selectors['product_name']),
            'price': self.clean_price(self.extract_data(response, selectors['price'])),
            'image_url': self.extract_data(response, selectors['image_url']),
            'product_url': response.url,
            'category': self.extract_category_from_url(response.url),  # Extract category from URL
            'product_description': self.extract_data(response, selectors['product_description']),
        }
    
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
    def clean_price(price: str) -> float:
        """Convert price string to float"""
        if not price:
            return None
        # Remove currency symbol and convert to float
        try:
            return float(price.replace('R', '').replace(',', '.').strip())
        except ValueError:
            return None
    
    @staticmethod
    def extract_category_from_url(url: str) -> str:
        """Extract category from the URL"""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        # Assuming the category is the third segment in the URL path
        if len(path_parts) > 3:
            return path_parts[2]  
        return 'Unknown'
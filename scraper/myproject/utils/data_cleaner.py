import re
from typing import Optional, Union

class DataCleaner:
    @staticmethod
    def clean_text(text: Optional[str]) -> Optional[str]:
        """Clean text by removing extra whitespace and special characters"""
        if not text:
            return None
        # Remove extra whitespace and normalize
        cleaned = ' '.join(text.split())
        # Remove special characters but keep basic punctuation
        cleaned = re.sub(r'[^\w\s.,!?-]', '', cleaned)
        return cleaned.strip()
    
    @staticmethod
    def clean_url(url: Optional[str]) -> Optional[str]:
        """Clean and validate URL"""
        if not url:
            return None
        # Remove whitespace
        url = url.strip()
        # Ensure URL starts with http/https
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    @staticmethod
    def clean_price(price: Union[str, float]) -> Optional[float]:
        """Clean price data"""
        if isinstance(price, float):
            return round(price, 2)
        if not price or not isinstance(price, str):
            return None
            
        try:
            # Remove currency symbols and whitespace
            cleaned = re.sub(r'[R$€£\s]', '', price)
            # Replace commas with dots for decimal
            cleaned = cleaned.replace(',', '.')
            # Convert to float and round to 2 decimal places
            return round(float(cleaned), 2)
        except ValueError:
            return None
    
    @staticmethod
    def clean_category(category: Optional[str]) -> str:
        """Clean category names"""
        if not category:
            return "Unknown"
        # Remove special characters and extra whitespace
        cleaned = re.sub(r'[^\w\s-]', '', category)
        cleaned = ' '.join(cleaned.split())
        return cleaned.title()

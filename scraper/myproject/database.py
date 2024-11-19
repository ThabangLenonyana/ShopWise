import pyodbc
from typing import Dict, Any
import logging
from dotenv import load_dotenv
import os

class AzureDBPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None
        load_dotenv()
        
    def connect_to_db(self):
        """Connect to Azure SQL Database"""
        try:
            connection_string = (
                f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
                f"SERVER={os.getenv('DB_SERVER')};"
                f"DATABASE={os.getenv('DB_NAME')};"
                f"UID={os.getenv('DB_USERNAME')};"
                f"PWD={os.getenv('DB_PASSWORD')};"
                f"Encrypt={os.getenv('DB_ENCRYPT')};"
                f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
                f"Connection Timeout={os.getenv('DB_CONNECTION_TIMEOUT')};"
            )
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
            self._ensure_tables_exist()
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def _ensure_tables_exist(self):
        """Check if tables exist and create them if they don't"""
        try:
            # Recreate tables with modified column lengths
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'retailers')
                CREATE TABLE [retailers] (
                    [id] integer IDENTITY(1,1) PRIMARY KEY,
                    [name] nvarchar(255),
                    [created_at] DATETIME2 DEFAULT GETDATE()
                )
            """)

            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'categories')
                CREATE TABLE [categories] (
                    [id] integer IDENTITY(1,1) PRIMARY KEY,
                    [name] nvarchar(255),
                    [created_at] DATETIME2 DEFAULT GETDATE()
                )
            """)

            # Modified products table with longer URL fields
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'products')
                CREATE TABLE [products] (
                    [id] integer IDENTITY(1,1) PRIMARY KEY,
                    [name] nvarchar(500),
                    [image_url] nvarchar(2000),
                    [product_url] nvarchar(2000),
                    [description] nvarchar(max),
                    [category_id] integer,
                    [retailer_id] integer,
                    [created_at] DATETIME2 DEFAULT GETDATE(),
                    FOREIGN KEY ([retailer_id]) REFERENCES [retailers] ([id]),
                    FOREIGN KEY ([category_id]) REFERENCES [categories] ([id])
                )
            """)

            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'prices')
                CREATE TABLE [prices] (
                    [id] integer IDENTITY(1,1) PRIMARY KEY,
                    [product_id] integer,
                    [price] float,
                    [created_at] DATETIME2 DEFAULT GETDATE(),
                    FOREIGN KEY ([product_id]) REFERENCES [products] ([id])
                )
            """)
            
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            self.conn.rollback()
            raise

    def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
        """Process and store item in Azure SQL Database"""
        try:
            if not self.conn:
                self.connect_to_db()
                
            # Process each component
            retailer_id = self._get_or_create_retailer(item['retailer'])
            category_id = self._get_or_create_category(item['category'])
            product_id = self._upsert_product(item, retailer_id, category_id)
            self._insert_price(product_id, item['price'])
            
            self.conn.commit()
            return item
            
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"Error processing item: {e}")
            raise

    def _get_or_create_retailer(self, retailer_name: str) -> int:
        """Get or create retailer and return id"""
        try:
            # Check if retailer exists
            self.cursor.execute("SELECT id FROM retailers WHERE name = ?", (retailer_name,))
            result = self.cursor.fetchone()
            
            if result:
                return result[0]
            
            # Create new retailer if it doesn't exist
            self.cursor.execute(
                "INSERT INTO retailers (name) OUTPUT INSERTED.id VALUES (?)",
                (retailer_name,)
            )
            return self.cursor.fetchone()[0]
            
        except Exception as e:
            logging.error(f"Error in _get_or_create_retailer: {e}")
            raise

    def _get_or_create_category(self, category_name: str) -> int:
        """Get or create category and return id"""
        try:
            # Check if category exists
            self.cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            result = self.cursor.fetchone()
            
            if result:
                return result[0]
            
            # Create new category if it doesn't exist
            self.cursor.execute(
                "INSERT INTO categories (name) OUTPUT INSERTED.id VALUES (?)",
                (category_name,)
            )
            return self.cursor.fetchone()[0]
            
        except Exception as e:
            logging.error(f"Error in _get_or_create_category: {e}")
            raise

    def _upsert_product(self, item: Dict[str, Any], retailer_id: int, category_id: int) -> int:
        """Insert or update product and return id"""
        try:
            # Check if product exists based on product_url
            self.cursor.execute(
                "SELECT id FROM products WHERE product_url = ?",
                (item['product_url'],)
            )
            result = self.cursor.fetchone()
            
            if result:
                # Update existing product
                self.cursor.execute("""
                    UPDATE products 
                    SET name = ?, image_url = ?, description = ?, 
                        category_id = ?, retailer_id = ?
                    WHERE id = ?
                """, (
                    item['product_name'], item['image_url'],
                    item.get('product_description', ''),
                    category_id, retailer_id, result[0]
                ))
                return result[0]
            
            # Insert new product
            self.cursor.execute("""
                INSERT INTO products (name, image_url, product_url, description, 
                                    category_id, retailer_id)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item['product_name'], item['image_url'], item['product_url'],
                item.get('product_description', ''),
                category_id, retailer_id
            ))
            return self.cursor.fetchone()[0]
            
        except Exception as e:
            logging.error(f"Error in _upsert_product: {e}")
            raise

    def _insert_price(self, product_id: int, price: float) -> None:
        """Insert new price record"""
        try:
            self.cursor.execute(
                "INSERT INTO prices (product_id, price) VALUES (?, ?)",
                (product_id, price)
            )
        except Exception as e:
            logging.error(f"Error in _insert_price: {e}")
            raise

    def close_spider(self, spider):
        """Close database connection when spider closes"""
        if self.conn:
            self.conn.close()
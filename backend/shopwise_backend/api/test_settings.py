from api.models import Products, Categories, Retailers, Prices
from accounts.models import User

# Override managed settings for testing
Products._meta.managed = True
Categories._meta.managed = True
Retailers._meta.managed = True
Prices._meta.managed = True
User._meta.managed = True
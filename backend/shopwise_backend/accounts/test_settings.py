from accounts.models import User

# Override managed setting for testing
User._meta.managed = True
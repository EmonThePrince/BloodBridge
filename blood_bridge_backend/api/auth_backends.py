from django.contrib.auth.backends import ModelBackend
from .models import Donor

class ContactAuthBackend(ModelBackend):
    def authenticate(self, request, contact=None, password=None, **kwargs):
        print(f"Authenticate called with contact={contact}")
        try:
            user = Donor.objects.get(contact=contact)
            print("User found:", user)
            if user.check_password(password):
                print("Password correct")
                return user
            else:
                print("Password incorrect")
        except Donor.DoesNotExist:
            print("Donor does not exist")
        return None
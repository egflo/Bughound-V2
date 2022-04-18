from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User

from Bughound.models import Employee


class BughoundBackend(BaseBackend):
    def authenticate(self, request=None, username=None, password=None, **kwars):
        #Here define you login criteria, like encrypting the password and then
        #Checking it matches. This is an example:
        try:
            print("BughoundBackend.authenticate()")
            user = User.objects.get(username=username)
            #user_password = make_password(password)
            #print("user_password: ", user_password)
            #username = user.username
            #password = user.password
            #email = '%s@bughound.com' % username
            #userlevel = user.userlevel
            #new_user = User.objects.create_user(username, email, password, is_active=True, is_staff=True, is_superuser=False)
            #User.save(new_user)
        except User.DoesNotExist:
            return None
        if check_password(password, user.password):
            if user.is_active:
                return user
            return None
        else:
            return None

    def get_user(self, user_id):
        #This shall return the user given the id
        from django.contrib.auth.models import AnonymousUser
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                return user
        except User.DoesNotExist:
            return None

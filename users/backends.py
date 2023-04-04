from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailUsernameAuthenticateBackend(ModelBackend):
    def authenticate(
        self,
        request,
        username=None,
        password=None,
        email=None,
        **kwargs,
    ):
        user_model = get_user_model()

        try:
            # to make django-admin work
            if username:
                user = user_model.objects.get(email=username)

            elif email:
                user = user_model.objects.get(email=email)

            else:
                raise user_model.DoesNotExist()

        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

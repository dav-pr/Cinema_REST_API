from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailUsernameAuthenticateBackend(ModelBackend):
    """Backend для аутентифікації користувачів за email або username.

    Методи:
    - authenticate: аутентифікація користувача за email або username та паролем.

    Аргументи authenticate:
    - request: запит, що надходить від користувача.
    - username: ім'я користувача (якщо використовується).
    - password: пароль користувача.
    - email: електронна пошта користувача (якщо використовується).
    - **kwargs: додаткові аргументи.

    Повертає:
    - User: об'єкт користувача, якщо аутентифікація пройшла успішно.
    - None: якщо аутентифікація не вдалась.
    """

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        email=None,
        **kwargs,
    ):
        """Аутентифікація користувача за email або username та паролем.

        Аргументи:
        - request: запит, що надходить від користувача.
        - username: ім'я користувача (якщо використовується).
        - password: пароль користувача.
        - email: електронна пошта користувача (якщо використовується).
        - **kwargs: додаткові аргументи.

        Повертає:
        - User: об'єкт користувача, якщо аутентифікація пройшла успішно.
        - None: якщо аутентифікація не вдалась.
        """
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

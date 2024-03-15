from django.contrib.auth import get_user_model


class EmailBackend:
    def authenticate(self, request, email=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

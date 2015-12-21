from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    name = "social"

    def ready(self):
        import social.signals
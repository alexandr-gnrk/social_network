from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # Импортируем файл с описанной функцией-подписчиком на сигнал.
        import images.signals
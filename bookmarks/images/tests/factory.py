from datetime import datetime

import factory, factory.django
from django.contrib.auth.hashers import make_password
from faker import Factory
from django.contrib.auth.models import User
from images.models import Image

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'password')

    username = 'user'  # faker.name()   # 'user'
    password = 'test'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        kwargs['password'] = make_password(kwargs['password'])
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image
        django_get_or_create = ('user', 'id', 'title', 'slug')

    user = factory.SubFactory(UserFactory)
    id = 1
    title = 'django'  # faker.word()
    slug = 'django'

    @factory.post_generation
    def users_like(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of users_like were passed in, use them
            for like in extracted:
                self.users_like.add(like)

    # url = 'images/2021/02/26/tv.jpg'
    # image = factory.LazyAttribute(
    #     lambda _: ContentFile(
    #         factory.django.ImageField()._make_data(
    #             {'width': 1024, 'height': 768}
    #         ), 'example.jpg'
    #     )
    # )
    # description = faker.text()
    # created = factory.LazyFunction(datetime.now)

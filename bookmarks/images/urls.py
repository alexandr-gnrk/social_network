from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ImageViewSet, ImageCreateView, ImageRankingView

app_name = 'images'

router = SimpleRouter()

router.register(r'api', ImageViewSet, basename='api')

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('ranking/', views.image_ranking, name='ranking'),
    path('', views.image_list, name='list'),
    # api
    path('api-ranking/', ImageRankingView.as_view()),
    path('api-create/', ImageCreateView.as_view()),
]

urlpatterns += router.urls

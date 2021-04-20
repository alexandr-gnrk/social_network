from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ImageViewSet, ImageCreateView, ImageRankingView, ImageLikeView

app_name = 'images'

router = SimpleRouter()

router.register(r'api', ImageViewSet, basename='api')

urlpatterns = [
    path('api/ranking/', ImageRankingView.as_view()),
    path('api/create-image/', ImageCreateView.as_view()),
    path('api/like/', ImageLikeView.as_view()),

    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('ranking/', views.image_ranking, name='ranking'),
    path('', views.image_list, name='list'),
]

urlpatterns += router.urls

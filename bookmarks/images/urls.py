from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ImageViewSet

app_name = 'images'

router = SimpleRouter()

router.register(r'api', ImageViewSet, basename='api')
# router.register(r'api-image-like', ImageLikeView, basename='api-image-like')
# router.register(r'api-actions', ActionViewSet, basename='api-actions')

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('ranking/', views.image_ranking, name='ranking'),
    path('', views.image_list, name='list'),

    # path('api-images/', ImageListView.as_view()),
    # path('api-images/<int:id>/<slug:slug>/', ImageDetailView.as_view()),
    # path('api-images/ranking/', ImageRankingView.as_view()),
    # path('api-create/', ImageCreateView.as_view()),
    # # path('api-like/', LikeView.as_view()),
    # # path('api-image-like/', ImageLikeView.as_view()),
    # path('api-action/', ActionView.as_view()),
]

urlpatterns += router.urls
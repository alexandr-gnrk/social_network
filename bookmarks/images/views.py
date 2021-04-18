from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from account.models import Profile
from sub.permissions import allowed_users, IsAuthenticatedAndSubscriber
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from actions.utils import create_action

import redis
from django.conf import settings
import stripe

from .serializers import ImageSerializer, ImageDetailSerializer, ImageCreateSerializer, ImageRankingSerializer, \
    ImageLikeSerializer

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    ordering = ['-created']
    ordering_fields = ['user', 'title', 'created', 'users_like', 'total_likes']
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object()
        # Увеличиваем количество просмотров картинки на 1.
        total_views = r.incr('image:{}:views'.format(image.id))
        # Увеличиваем рейтинг картинки на 1.
        r.zincrby('image_ranking', image.id, 1)

        users_like = image.users_like.values_list(flat=True)
        users_like_photo = []
        for user_id in users_like:
            user_photo = Profile.objects.get(id=user_id).photo
            users_like_photo.append(str(user_photo))

        serializer = ImageDetailSerializer(image, context={
            'total_views': total_views,
            'users_like_photo': users_like_photo
        })
        return Response(serializer.data)


class ImageRankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем набор рейтинга картинок.
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        # Получаем отсортированный список самых популярных картинок.
        most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

        serializer = ImageRankingSerializer(most_viewed, many=True)
        return Response(serializer.data)


class ImageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedAndSubscriber]

    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # create_action(request.user, 'bookmarked image', serializer)
        return Response(serializer.data)


class ImageLikeView(APIView):

    def post(self, request):
        serializer = ImageLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            action = serializer.validated_data['action']
            image_id = serializer.validated_data['id']
            if image_id and action:
                try:
                    image = Image.objects.get(id=image_id)
                    if action == 'like':
                        image.users_like.add(user)
                        create_action(user, 'likes', image)
                    else:
                        image.users_like.remove(user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    pass
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
@allowed_users(allowed_roles=['subscribers'])
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны.
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            print('New item', new_item)
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET-запроса.
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Увеличиваем количество просмотров картинки на 1.
    total_views = r.incr('image:{}:views'.format(image.id))
    # Увеличиваем рейтинг картинки на 1.
    r.zincrby('image_ranking', image.id, 1)
    return render(request,
                  'images/image/detail.html',
                  {
                      'section': 'images',
                      'image': image,
                      'total_views': total_views,
                  })


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return Response({'status': 'ok'})
        except:
            pass
    return Response({'status': 'ok'})


@login_required
def image_list(request):
    images = Image.objects.all().order_by('-id')
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # Получаем набор рейтинга картинок.
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Получаем отсортированный список самых популярных картинок.
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images', 'most_viewed': most_viewed})

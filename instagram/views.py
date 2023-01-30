from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PostForm
from .models import Tag, Post


def index(request):
    timesince = timezone.now() - timedelta(days=3)
    post_list = Post.objects.all()\
        .filter(
        Q(author=request.user) |
        Q(author__in=request.user.following_set.all())
    )\
        .filter(created_at__gte=timesince)

    suggested_user_list = get_user_model().objects.all() \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=request.user.following_set.all())  # 현재 following한 사람들은 보여주지 않음
    return render(request, "instagram/index.html", {
        'post_list': post_list,
        'suggested_user_list': suggested_user_list[:5],  # 추천친구 5명까지만
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "포스팅을 저장했습니다")
            return redirect(post)
    else:
        form = PostForm()
    return render(request, "instagram/post_form.html", context={
        'form': form,
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        'post': post,
    })


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username)  # 해당 모델에 username 키워드 인자로 GET 요청
    post_list = Post.objects.filter(author=page_user)

    # 해당 유저가 follow 되어있는지 확인하는 변수
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(request, "instagram/user_detail.html", {
        'page_user': page_user,
        'post_list': post_list,
        'is_follow': is_follow,
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

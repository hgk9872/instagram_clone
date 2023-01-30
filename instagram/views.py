from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import PostForm
from .models import Tag, Post


def index(request):
    post_list = Post.objects.all()\
        .filter(
        Q(author=request.user) |
        Q(author__in=request.user.following_set.all())
    )

    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all()) # 현재 following한 사람들은 보여주지 않음
    return render(request, "instagram/index.html", {
        'post_list': post_list,
        'suggested_user_list': suggested_user_list[:5], # 추천친구 5명까지만
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
            return redirect(post)  # TODO: get_absolute_url 활용
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
    page_user = get_object_or_404(get_user_model(), username=username) # 해당 모델에 username 키워드 인자로 GET 요청
    post_list = Post.objects.filter(author=page_user)
    return render(request, "instagram/user_detail.html", {
        'page_user': page_user,
        'post_list': post_list,
    })

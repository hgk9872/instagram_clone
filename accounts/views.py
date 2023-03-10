from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, logout_then_login, PasswordChangeView
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileForm, CustomPasswordChangeForm
from .models import User


def logout(request):
    messages.success(request, '로그아웃되었습니다')
    return logout_then_login(request)


login = LoginView.as_view(template_name="accounts/login_form.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()  # 새로 가입한 유저
            auth_login(request, signed_user)
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천
            messages.success(request, "회원가입을 환영합니다")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 저장했습니다.")
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit_form.html', {
        'form': form,
    })


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, '암호를 변경했습니다.')
        return super().form_valid(form)


password_change = CustomPasswordChangeView.as_view()


@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username)
    request.user.following_set.add(follow_user) # 요청보낸 사람이 username 유저를 팔로우
    messages.success(request, f"{follow_user}님을 팔로우했습니다")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    request.user.following_set.remove(unfollow_user)
    messages.success(request, f"{unfollow_user}님을 언팔로우했습니다")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

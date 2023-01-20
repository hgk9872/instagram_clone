from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()  # 새로 가입한 유저
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천
            messages.success(request, "회원가입을 환영합니다")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

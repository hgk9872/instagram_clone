from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from .models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']  # 유효성 검사 후, 통과된 데이터 get
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile', 'first_name', 'last_name', 'website_url', 'phone_number', 'gender']


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요.")
        return new_password2

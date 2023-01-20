from django.contrib.auth import forms
from .models import User


class SignupForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']  # 유효성 검사 후, 통과된 데이터 get
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다")
        return email

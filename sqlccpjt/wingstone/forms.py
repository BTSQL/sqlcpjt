
from django.forms import EmailField, CharField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


# email 필드를 정상적으로 출력이 되도록 수정이 필요함
class SqlcUserCreationForm(UserCreationForm):
    username = EmailField(label='email', required=True)
    #contact_num = CharField(label='-빼고 입력하세요', max_length=16, min_length=10)


    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': '이메일',
                                                'id': 'email',
                                                'name': 'email',
                                                'class': 'mail'}),
        }

    def save(self, commit=True):
        user = super(SqlcUserCreationForm,self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["username"]
     #user.username = self.cleaned_data["username"]
        if commit :
            user.save()
        return user

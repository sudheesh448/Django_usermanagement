from django import forms

from week9_app.models import user_db
class UserForm(forms.ModelForm):
    class Meta:
        model = user_db
        widgets = {
        'password': forms.PasswordInput(),
    }
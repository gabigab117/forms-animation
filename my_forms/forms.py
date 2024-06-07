from django import forms
from django_recaptcha.fields import ReCaptchaField

from my_forms.models import Article


class ArticleForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Article
        # fields = ['name', 'email']
        # fields = '__all__'
        exclude = ['author']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters long')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if "patrick" in content:
            raise forms.ValidationError('patrick is not allowed')
        return content

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and content and title not in content:
            raise forms.ValidationError('title must be in content')
        return cleaned_data


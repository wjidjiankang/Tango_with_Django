from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
# 80 - 第 7 章 表单
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
# 25 # 把这个 ModelForm 与一个模型连接起来
        model = Page
# 27
# 28 # 想在表单中放哪些字段？
# 29 # 有时不需要全部字段
# 30 # 有些字段接受空值，因此可能无需显示
# 31 # 这里我们想隐藏外键字段
# 32 # 为此，可以排除 category 字段
        exclude = ('category',)
# 34 # 也可以直接指定想显示的字段（不含 category 字段）
# 35 # fields = ('title', 'url', 'views'
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # 如果 url 字段不为空，而且不以“http://”开头
        # 在前面加上“http://
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
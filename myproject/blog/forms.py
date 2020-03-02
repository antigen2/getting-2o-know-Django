from django import forms


class EmailPostForm(forms.Form):
    # 25 - максимальная длинна поля
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # required=False - необязательное поле
    # widget=forms.Textarea - html-элемент text-area (input-по умолчанию)
    comments = forms.CharField(required=False, widget=forms.Textarea)

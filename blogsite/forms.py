from django import forms
from blogsite.models import Post

class NewPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['post_header'].label = 'Заголовок поста'
        self.fields['post_text'].label = 'Содержание поста'

    class Meta:
        model = Post
        fields = (
            'post_header',
            'post_text',
        )

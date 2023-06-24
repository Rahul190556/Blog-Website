from django import forms
from app.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("author", "title", "text")
        widgets = {
            "title": forms.Textarea(attrs={"class": "textinputclass"}),
            "text": forms.Textarea(
                attrs={"class": "editable medium-editor-textarea postcontent"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author", "text")

        # Theses widgets are used in css files
        widgets = {
            "text": forms.Textarea(attrs={"class": "editable medium-editor-textarea"}),
        }


# By specifying these widgets in the form, you can control the appearance and behavior of the form fields in the
# rendered HTML, such as applying custom CSS classes, adding JavaScript libraries, or enabling rich text editing capabilities.

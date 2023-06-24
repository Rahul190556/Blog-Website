from django.db import models
from django.utils import timezone
from django.urls import reverse


# By using "auth.User", you are providing a string representation of the model's path (app_name.ModelName) instead
# of directly importing the User model. This is done to avoid circular import errors when defining relationships between models.
class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # By using self, you can access and modify the attributes and fields of the current instance within its methods.
    #  It allows you to perform operations on the specific instance that the method is being called on.

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


# By providing a meaningful __str__ method, it becomes easier to identify and work with instances of the Post model
# when dealing with them in the code or debugging. It helps improve readability and makes the output more informative.


class Comment(models.Model):
    post = models.ForeignKey(
        "app.Post", related_name="comments", on_delete=models.CASCADE
    )
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("app:post_list")

    def __str__(self):
        return self.text


# By specifying related_name='comments', you are customizing the reverse relation from Post to Comment.
#  Now, you can access the comment posted by author using the comment attribute, like post.comments.all().

# In Django, the reverse() function is used to generate URLs for a given view.
# It takes the view name or URL pattern as an argument and returns the corresponding URL.

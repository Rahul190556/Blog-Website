from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Post, Comment
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from app.forms import PostForm, CommentForm

# Create your views here.
# the model attribute in views.py is essential to define the connection between the view and the
# associated model, enabling the use of built-in functionality and promoting code organization and reusability.


class AboutView(TemplateView):
    template_name = "app/blog/about.html"


class PostListView(ListView):
    model = Post
    template_name = "app/blog/post_list.html"

    # lte is less than or equal to
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "app/blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    template_name = "app/blog/post_form.html"
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Set the author of the post as the current user
        form.instance.author = self.request.user
        # Save the form and get the post object
        post = form.save()
        # Redirect to the post detail page using the post's ID
        return redirect(reverse("app:post_detail", kwargs={"pk": post.pk}))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    template_name = "app/blog/post_form.html"
    form_class = PostForm
    model = Post

    def get_success_url(self):
        return reverse_lazy("app:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "app/blog/post_confirm_delete.html"
    success_url = reverse_lazy("app:post_list")


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    login_url = "/login/"
    redirect_field_name = "app:post_list"
    template_name = "app/blog/post_draft_list.html"
    context_object_name = "posts"  # Specify the variable name for the object list

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by("created_date")


# additional way to add posts variable which used in templates
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context[
#         "posts"
#     ] = self.get_queryset()  # Add the 'posts' variable to the context
#     return context

# get_context_data() in your views to add any additional data you need in the context dictionary,
# providing more flexibility in manipulating and passing data to your templates.

# Using get_object_or_404() helps simplify the code by handling the common case of object retrieval and error handling in a single line.


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("app:post_detail", pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("app:post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "app/blog/comment_form.html", {"form": form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved_comment = True
    comment.save()
    return redirect("app:post_detail", pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("app:post_detail", pk=post_pk)


# if the pk value is 42, the constructed URL would be something like "/post/42/".
# This ensures that the user is redirected to the correct post_detail page of the published post.

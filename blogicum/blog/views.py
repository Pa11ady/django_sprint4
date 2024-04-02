from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .constants import PER_PAGE
from .forms import CommentForm
from .mixins import AuthorizationMixin, CommentMixin, PostMixin
from .models import Category, Comment, Post
from .utils import get_page_obj, get_posts

User = get_user_model()


def index(request):
    template = 'blog/index.html'
    page_number = request.GET.get('page')
    context = {
        'page_obj': get_page_obj(get_posts(), page_number)
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=pk
    )
    if post.author != request.user:
        post = get_object_or_404(
            get_posts(),
            pk=pk
        )
    context = {
        'post': post,
        'comments': post.comments.all(),
        'form': CommentForm()
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    page_number = request.GET.get('page')
    context = {
        'category': category,
        'page_obj': get_page_obj(get_posts(category.posts), page_number)
    }
    return render(request, template, context)


class ProfileListView(ListView):
    model = Post
    paginate_by = PER_PAGE
    template_name = 'blog/profile.html'

    def get_user(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        author = self.get_user()
        if author == self.request.user:
            return author.posts.all()
        return get_posts(author.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostUpdateView(PostMixin, AuthorizationMixin, UpdateView):
    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(PostMixin, AuthorizationMixin, DeleteView):
    success_url = reverse_lazy('blog:index')


@login_required
def add_comment(request, post_id, comment_id=None):
    post = get_object_or_404(
        Post,
        pk=post_id
    )
    if request.method == 'POST':
        if comment_id:
            form = CommentForm(
                instance=Comment.objects.get(pk=comment_id),
                data=request.POST
            )
        else:
            form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_id)


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass

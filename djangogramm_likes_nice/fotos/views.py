from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.db.models import F
from django.views import View
from django.http import JsonResponse
import random

from fotos.forms import RegisterUserForm, LoginUserForm, EditProfileForm

from fotos.models import Fotos, Like, Follow

# Create your views here.

menu = [{'title': 'My subscriptions', 'url_name': 'my_subscriptions'},
        {'title': 'My photos', 'url_name': 'my_photos'},
        {'title': 'My followers', 'url_name': 'my_followers'},
        {'title': 'User profile', 'url_name': 'user_profile'},
        {'title': 'Feedback', 'url_name': 'feedback'},
        ]


class MainPage(View):

    def post(self, request, *args, **kwargs):
        my_ids = User.objects.values_list('id', flat=True)
        my_ids = list(my_ids)
        num_of_users = 3
        random_ids = random.sample(my_ids, num_of_users)
        user = User.objects.filter(id__in=random_ids)
        fotos = Fotos.objects.filter(user_id__in=random_ids)
        active_user = request.user.id

        if request.method == 'POST' and 'btnlike' in request.POST:
            foto_id = request.POST.get('foto_id')
            if Like.objects.filter(user_id=active_user,
                                   photo_id=foto_id).exists():
                like_obj = Like.objects.filter(user_id=active_user,
                                               photo_id=foto_id).delete()
                Fotos.objects.filter(id=foto_id).update(liked=F('liked') - 1)
            else:
                like_obj = Like.objects.create(value='Like',
                                               user_id=active_user,
                                               photo_id=foto_id)
                Fotos.objects.filter(id=foto_id).update(liked=F('liked') + 1)
                like_obj.save()

        if request.method == 'POST' and 'btnfollow' in request.POST:
            author_id = request.POST.get('author_id')
            if Follow.objects.filter(author_id=author_id,
                                     user_id=active_user).exists():
                follow_obj = Follow.objects.filter(author_id=author_id).\
                    delete()
            else:
                follow_obj = Follow.objects.create(author_id=author_id,
                                                   user_id=active_user)
                follow_obj.save()

        context = {
            'user_data': user,
            'fotos': fotos,
            'menu': menu,
            'title': 'Main page'
        }
        return render(request,
                      'fotos/main_page.html',
                      context=context
                      )

    def get(self, request, *args, **kwargs):
        my_ids = User.objects.values_list('id', flat=True)
        my_ids = list(my_ids)
        num_of_users = 3
        random_ids = random.sample(my_ids, num_of_users)
        user = User.objects.filter(id__in=random_ids)
        fotos = Fotos.objects.filter(user_id__in=random_ids)
        context = {
            'user_data': user,
            'fotos': fotos,
            'menu': menu,
            'title': 'Main page'
        }
        return render(request,
                      'fotos/main_page.html',
                      context=context
                      )


class MySubscriptions(View):
    template_name = 'fotos/my_subscriptions.html'

    def post(self, request, *args, **kwargs):
        active_user = request.user.id
        like = Like.objects.all()

        if request.method == 'POST' and 'btnlike' in request.POST:
            foto_id = request.POST.get('foto_id')
            if Like.objects.filter(user_id=active_user,
                                   photo_id=foto_id).exists():
                like_obj = Like.objects.filter(user_id=active_user,
                                               photo_id=foto_id).delete()
                Fotos.objects.filter(id=foto_id).update(liked=F('liked') - 1)
            else:
                like_obj = Like.objects.create(value='Like',
                                               user_id=active_user,
                                               photo_id=foto_id)
                Fotos.objects.filter(id=foto_id).update(liked=F('liked') + 1)
                like_obj.save()

        if request.method == 'POST' and 'btnfollow' in request.POST:
            author_id = request.POST.get('author_id')
            if Follow.objects.filter(author_id=author_id,
                                     user_id=active_user).exists():
                follow_obj = Follow.objects.filter(author_id=author_id).\
                    delete()
            else:
                follow_obj = Follow.objects.create(author_id=author_id,
                                                   user_id=active_user)
                follow_obj.save()

        subscriptions = Follow.objects.filter(user_id=active_user)
        subscriptions_ids = subscriptions.values_list('author_id')
        users_i_follow = User.objects.filter(id__in=subscriptions_ids)
        fotos = Fotos.objects.filter(user_id__in=subscriptions_ids)

        context = {
            'fotos': fotos,
            'like': like,
            'menu': menu,
            'users_i_follow': users_i_follow,
            'title': 'Subscriptions',
        }

        return render(request,
                      self.template_name,
                      context=context
                      )

    def get(self, request, *args, **kwargs):
        like = Like.objects.all()
        active_user = request.user.id
        subscriptions = Follow.objects.filter(user_id=active_user)
        subscriptions_ids = subscriptions.values_list('author_id')
        users_i_follow = User.objects.filter(id__in=subscriptions_ids)
        fotos = Fotos.objects.filter(user_id__in=subscriptions_ids)
        context = {
            'fotos': fotos,
            'like': like,
            'menu': menu,
            'users_i_follow': users_i_follow,
            'title': 'Subscriptions',
        }

        return render(request,
                      self.template_name,
                      context=context
                      )


class Feedback(View):

    def get(self, request, *args, **kwargs):
        return render(request,
                      'fotos/feedback.html',
                      {'menu': menu, 'title': 'Feedback'}
                      )


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'fotos/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'fotos/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main_page')


class MyPhotos(View):
    template_name = 'fotos/my_photos.html'

    def post(self, request, *args, **kwargs):
        active_user = request.user.id
        fotos = Fotos.objects.filter(user_id=active_user)
        if request.method == 'POST' and 'btn_upload' in request.POST:
            foto_file = request.FILES.get('file')
            title = request.POST.get('title')
            description = request.POST.get('description')
            photo = Fotos.objects.create(user_id=active_user,
                                         photo=foto_file,
                                         title=title,
                                         description=description,
                                         )
            photo.save()
            return redirect(reverse('my_photos'))
        if request.method == 'POST' and 'btn_delete' in request.POST:
            foto_id = request.POST.get('foto_id')
            photo = Fotos.objects.get(id=foto_id)
            photo.delete()
            return redirect(reverse('my_photos'))
        else:
            args = {'menu': menu, 'fotos': fotos, 'title': 'My photos'}
            return render(request, self.template_name, args)

    def get(self, request, *args, **kwargs):
        active_user = request.user.id
        fotos = Fotos.objects.filter(user_id=active_user)
        args = {'menu': menu, 'fotos': fotos, 'title': 'My photos'}
        return render(request, self.template_name, args)


class MyFollower(View):

    def get(self, request, *args, **kwargs):
        active_user = request.user.id
        my_followers_ids = Follow.objects.filter(author_id=active_user)
        my_followers_names = User.objects.all()
        args = {'menu': menu,
                'my_followers_names': my_followers_names,
                'my_followers_ids': my_followers_ids,
                'title': 'My followers',
                }
        return render(request, 'fotos/my_followers.html', args)


class EditProfile(View):
    form_class = EditProfileForm
    template_name = 'fotos/user_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(instance=request.user)
            args = {'form': form, 'menu': menu, 'title': 'Update profile'}
            return render(request, self.template_name, args)
        else:
            args = {'menu': menu, 'title': 'Update profile'}
            return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect(reverse('user_profile'))
        else:
            args = {'menu': menu, 'title': 'Update profile'}
            return render(request, self.template_name, args)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> 404 Page not found </h1>')


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic

from google.appengine.api import users
from . import forms
from . import models


class LoginRequiredMixin(object):
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = None

    @method_decorator(login_required(redirect_field_name=redirect_field_name, login_url=login_url))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class BlogList(generic.ListView):
    queryset = models.Entry.objects.all()
    template_name = "list.html"
    paginate_by = 6


class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"


class BlogAddEntry(LoginRequiredMixin, generic.View):
    template_name = "edit.html"

    def get(self, request):
        form = forms.EntryForm(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.EntryForm(request.POST, request=request)
        if form.is_valid():
            newpost = form.save()
            return HttpResponseRedirect(reverse('entry-detail', args=[newpost.slug, ]))

        return render(request, self.template_name, {
            'form': form
        })


class BlogEditEntry(LoginRequiredMixin, generic.UpdateView):
    template_name = "edit.html"
    model = models.Entry
    form_class = forms.EntryForm

    def get_success_url(self):
        return reverse('list')


class BlogDeleteEntry(LoginRequiredMixin, generic.DeleteView):
    model = models.Entry
    template_name = "delete.html"

    def get_success_url(self):
        return reverse('list')


class LoginView(generic.View):
    def get(self, request):
        index = reverse('list')
        url = users.create_login_url(index)
        return HttpResponseRedirect(url)


class LogoutView(generic.View):
    def get(self, request):
        index = reverse('list')
        url = users.create_logout_url(index)
        return HttpResponseRedirect(url)

from django.views.generic import View
from django.http.response import HttpResponseForbidden


class GuestView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseForbidden()

        return super(GuestView, self).dispatch(request, *args, **kwargs)

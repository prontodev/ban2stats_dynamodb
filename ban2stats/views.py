from django.http.response import HttpResponse, HttpResponseBadRequest


def token_required(function):
    def inner(request, *args, **kwargs):
        if request.META.get('HTTP_TOKEN'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest("Token is required.")
    return inner

@token_required
def home(request):
    return HttpResponse(request.META['HTTP_TOKEN'])
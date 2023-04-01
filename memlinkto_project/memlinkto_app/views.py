from allauth.account.models import EmailAddress
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.defaults import page_not_found
from memlinkto_app.models import UrlMapping

def index(request):
    template_file = 'index.html'
    if request.user.is_authenticated:
        template_file = 'create.html'
    template = loader.get_template(template_file)
    return HttpResponse(template.render({}, request))


# Create your views here.
def create(request):
    template = loader.get_template('create.html')
    return HttpResponse(template.render({}, request))


def links(request):
    template = loader.get_template("links.html")
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mappings = UrlMapping.objects.filter(email_address=email_address)
    result = []
    for url_mapping in url_mappings:
        entry = {"short_url": url_mapping.short_url, "long_url": url_mapping.long_url}
        result.append(entry)
    return HttpResponse(template.render({"url_mappings": result}, request))

def redirect_or_404(request, exception):
    url_mappings = UrlMapping.objects.filter(short_url=request.build_absolute_uri())
    if len(url_mappings) > 0:
        return redirect(url_mappings[0].long_url)
    return page_not_found()

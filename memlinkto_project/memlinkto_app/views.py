from allauth.account.models import EmailAddress
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.defaults import page_not_found
from memlinkto_app.models import UrlMapping
import requests
from bs4 import BeautifulSoup
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
from slugify import slugify
import re

tf.disable_v2_behavior()
text_generator = hub.Module('/Users/jeetub/Downloads/roberta24')

# Create placeholders for the input data
input_placeholder = tf.placeholder(dtype=tf.string, shape=[None])

# Apply the module to the input data
output_summaries = text_generator(input_placeholder)

# Create a TensorFlow session
session = tf.Session()
session.run(tf.global_variables_initializer())
session.run(tf.tables_initializer())

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


def generate_slug(url):
    html = requests.get(url).text
    text_content = BeautifulSoup(html, 'html.parser').get_text()
    summaries = session.run(output_summaries, feed_dict={input_placeholder: [text_content]})
    summary = summaries[0].decode('utf-8')
    summary_no_articles = ' '.join(
        [word for word in re.findall(r'\b\w+\b', summary) if word.lower() not in ['a', 'an', 'the']])
    return slugify(summary_no_articles)

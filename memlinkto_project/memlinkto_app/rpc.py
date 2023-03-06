from allauth.account.models import EmailAddress
from modernrpc.core import rpc_method, REQUEST_KEY
import uuid

from memlinkto_app.models import UrlMapping


@rpc_method
def suggest_link(long_url: str):
    short_url = "https://memlink.to/" + uuid.uuid4().hex.upper()[0:6]
    return short_url


@rpc_method
def create_link(short_url: str, long_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mapping = UrlMapping(email_address=email_address, short_url=short_url, long_url=long_url)
    url_mapping.save()
    return short_url


@rpc_method
def fetch_link(short_url: str):
    url_mapping: UrlMapping = UrlMapping.objects.get(short_url=short_url)
    return url_mapping.long_url

@rpc_method
def delete_link(short_url: str, long_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mapping = UrlMapping(email_address=email_address, short_url=short_url, long_url=long_url)
    url_mapping.save()
    return short_url
@rpc_method
def list_links(**kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mappings = UrlMapping.objects.filter(email_address=email_address)
    return list(map(lambda x: {"short_url": x.short_url, "long_url": x.long_url}, list(url_mappings)))

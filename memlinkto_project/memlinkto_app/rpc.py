from allauth.account.models import EmailAddress
from modernrpc.core import rpc_method, REQUEST_KEY
import uuid

from memlinkto_app.models import UrlMapping

@rpc_method
def create_link(long_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    # check if long url is already saved for the given user.
    url_mappings = UrlMapping.objects.filter(email_address=email_address, long_url=long_url)
    if len(url_mappings) > 0:
        return url_mappings[0].short_url
    # generate a new short url if it is a new long url for the given user.
    short_url = "https://memlink.to/" + uuid.uuid4().hex.upper()[0:6]
    url_mapping = UrlMapping(email_address=email_address, short_url=short_url, long_url=long_url)
    url_mapping.save()
    return short_url


@rpc_method
def fetch_link(short_url: str):
    url_mapping: UrlMapping = UrlMapping.objects.get(short_url=short_url)
    return url_mapping.long_url

@rpc_method
def delete_link(short_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address: EmailAddress = EmailAddress.objects.get(user_id=request.user)
    url_mapping: UrlMapping = UrlMapping.objects.get(email_address=email_address, short_url=short_url)
    url_mapping.delete()
    return short_url

@rpc_method
def list_links(**kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mappings = UrlMapping.objects.filter(email_address=email_address)
    result = []
    for url_mapping in url_mappings:
        entry = {"short_url": url_mapping.short_url, "long_url": url_mapping.long_url}
        result.append(entry)
    return result

from allauth.account.models import EmailAddress
from modernrpc.core import rpc_method, REQUEST_KEY
import uuid
import requests
import json

from memlinkto_app.models import UrlMapping


@rpc_method
def create_link(long_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    # check if long url is already saved for the given user.
    url_mappings = UrlMapping.objects.filter(
        email_address=email_address, long_url=long_url)
    if len(url_mappings) > 0:
        return url_mappings[0].short_url
    try:
        response = requests.post("http://ec2-35-84-2-187.us-west-2.compute.amazonaws.com:8080/slug", json={
            "url": long_url}, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        slug = uuid.uuid4().hex.upper()[0:6]
    else:
        slug = response.json()['slug']
    short_url = "https://memlink.to/" + slug
    url_mapping = UrlMapping(email_address=email_address,
                             short_url=short_url, long_url=long_url)
    url_mapping.save()
    return short_url


@rpc_method
def link_is_safe(input_url: str):
    api_key = 'AIzaSyDzJERZizEEmzTCkLoScuygU_gtCnKT2dA'
    url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'

    # Define the request body as a dictionary
    request_body = {
        'client': {
            'clientId':      'memlink-to',
            'clientVersion': '0.0.1'
        },
        'threatInfo': {
            'threatTypes':      ['MALWARE', 'SOCIAL_ENGINEERING', 'POTENTIALLY_HARMFUL_APPLICATION'],
            'platformTypes':    ['WINDOWS'],
            'threatEntryTypes': ['URL'],
            'threatEntries':    [{'url': input_url}]
        }
    }

    # Convert the request body to a JSON string
    json_data = json.dumps(request_body)

    # Make the request with the appropriate headers
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json_data)

    # Check if the request was successful and process the response
    if response.status_code == 200:
        response_data = response.json()
        # Process the response data as needed
        if not response_data:
            print("Site is safe")
            return "safe"
        else:
            threat_matches = response_data.get('matches', [])
            for match in threat_matches:
                print(f'Site not safe, Threat type: {match["threatType"]}')
            return "not safe"
    else:
        print(f'Request failed with status code {response.status_code}')
        return "failed"


@ rpc_method
def fetch_link(short_url: str):
    url_mapping: UrlMapping = UrlMapping.objects.get(short_url=short_url)
    return url_mapping.long_url


@ rpc_method
def delete_link(short_url: str, **kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address: EmailAddress = EmailAddress.objects.get(
        user_id=request.user)
    url_mapping: UrlMapping = UrlMapping.objects.get(
        email_address=email_address, short_url=short_url)
    url_mapping.delete()
    return short_url


@ rpc_method
def list_links(**kwargs):
    request = kwargs.get(REQUEST_KEY)
    email_address = EmailAddress.objects.get(user_id=request.user)
    url_mappings = UrlMapping.objects.filter(email_address=email_address)
    result = []
    for url_mapping in url_mappings:
        entry = {"short_url": url_mapping.short_url,
                 "long_url": url_mapping.long_url}
        result.append(entry)
    return result

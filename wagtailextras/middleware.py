import random
import re
import json

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.template import loader, RequestContext
from django.utils.encoding import smart_text, force_text
from django.utils.deprecation import MiddlewareMixin
from django.utils.html import escape


def is_html(response):
    """
    Returns True if the response is either `text/html` or `application/xhtml+xml`
    """
    content_type = response.get('Content-Type', None)
    return bool(content_type and content_type.split(';')[0] in ('text/html', 'application/xhtml+xml'))


class ObfuscateEmailAddressMiddleware(MiddlewareMixin):
    """
    Replaces plain email addresses with escaped addresses in (non streaming) HTML responses
    """
    def process_response(self, request, response):
        if is_html(response) and hasattr(response, 'content'):  # Do not obfuscate non-html and streaming responses.
            # https://emailregex.com/
            email_pattern = r'(?P<email>[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
            # Checks for emails:
            # - At start of the string
            # - Directly preceeded by a space
            # - Preceeded by a > which is not followed by a <
            # - Inside a href (optionally preceeded by mailto:)
            email_href_text = re.compile(r'(^|\s|>[^<]*?|(?<=href=[\'\"])(mailto:)?){email_pattern}'.format(email_pattern=email_pattern))
            response.content = email_href_text.sub(self.encode_email, force_text(response.content))

        return response

    def encode_email(self, matches):
        email = matches.group('email')
        encoded_email = ''.join(random.choice(['&#{:d};', '&#x{:x};']).format(ord(char)) for char in email)
        return matches.group().replace(email, encoded_email)


class ForceCsrfCookieMiddleware(MiddlewareMixin):
    """
    Forces the CSRF cookie to be set for each request
    """
    def process_request(self, request):
        get_token(request)

import random
import re
import json
from urllib import unquote

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.template import loader, RequestContext
from django.utils.encoding import smart_text
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
            # http://www.lampdocs.com/blog/2008/10/regular-expression-to-extract-all-e-mail-addresses-from-a-file-with-php/
            email_pattern = re.compile(r'(mailto:)?[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*(\+[_a-zA-Z0-9-]+)?@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(([0-9]{1,3})|([a-zA-Z]{2,3})|(aero|coop|info|museum|name))')
            response.content = email_pattern.sub(self.encode_email, response.content)
        return response

    def encode_email(self, matches):
        encoded_char_list = []
        for char in matches.group(0):
            encoded_char_list.append(random.choice(['&#%d;' % ord(char), '&#x%x;' % ord(char)]))
        return ''.join(encoded_char_list)


class ForceCsrfCookieMiddleware(MiddlewareMixin):
    """
    Forces the CSRF cookie to be set for each request
    """
    def process_request(self, request):
        get_token(request)

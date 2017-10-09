# Extras for wagtail

This app will add some necessities to wagtail:

## Install

    pip install wagtail-extras

Add `wagtailextras` to your installed apps:

    INSTALLED_APPS = [
        ...
        'wagtailextras',
        ...
    ]

For setup of individual parts, please continue below.

## ObfuscateEmailAddressMiddleware

Transforms emailaddresses to decimal/hexadecimal unicode character entities to foil bots trying to harvest emailaddress

### Setup

Add the following to the middleware:

    MIDDLEWARE = [
        ...
        'wagtailextras.middleware.ObfuscateEmailAddressMiddleware',
        ...
    ]

## ForceCsrfCookieMiddleware

Forces Django to create an CSRF token for you when you for example are using JavaScript forms.

### Setup

Add the following to the middleware:

    MIDDLEWARE = [
        ...
        'wagtailextras.middleware.ForceCsrfCookieMiddleware',
        ...
    ]

## Breadcrumbs

Returns an ordered list in the template, showing the current location.

### Usage

Load the template tag:

    {% load wagtailextras_tags %}

Write out the breadcrumbs in the html:

    {% breadcrumbs %}

## Main menu

A simple implementation showing the pagestructure of wagtail as a menu.

### Usage

Load the template tag:

    {% load wagtailextras_tags %}

Write out the menu in the html:

    {% get_site_root as site_root %}
    {% main_menu parent=site_root calling_page=self %}

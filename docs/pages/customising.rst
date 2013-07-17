#########################
Customising and extending
#########################


Extending templates
-------------------
Photologue comes with a set of basic templates to get you started quickly - you
can of course replace them with your own. That said, it is possible to extend the basic templates in 
your own project and override various blocks, for example to add css classes.
Often this will be enough.

The trick to extending the templates is not special to Photologue, it's used
in other projects such as `Oscar <https://django-oscar.readthedocs.org/en/latest/recipes/how_to_customise_templates.html>`_.

First, set up your template configuration as so::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...other template folders...,
        PHOTOLOGUE_APP_DIR
    )

The ``PHOTOLOGUE_APP_DIR`` points to the directory above Photologue's normal
templates directory.  This means that ``path/to/photologue/template.html`` can also
be reached via ``templates/path/to/photologue/template.html``.

For example, to customise ``photologue/gallery_list.html``, you can have an implementation like::

    # Create your own photologue/gallery_list.html
    {% extends "templates/photologue/gallery_list.html" %}

    ... we are now extending the built-in gallery_list.html and we can override
    the content blocks that we want to customise ...


Settings
--------
Photologue has several settings to customise behaviour; at present this part of the
documentation is unfortunately incomplete.

PHOTOLOGUE_USE_CKEDITOR
~~~~~~~~~~~~~~~~~~~~~~~
If you have already installed `django-ckeditor <https://pypi.python.org/pypi/django-ckeditor>`_
then you can use to edit the TextArea fields of Gallery
and Photo in the admin. Simply set the setting to ``True``. 

Third-party contributions
-------------------------
Photologue has a 'contrib' folder that includes some
useful tweaks to the base project.

Old-style templates
~~~~~~~~~~~~~~~~~~~
Replaces the normal templates with the templates that used to come with
Photologue 2.X. Use these if you have an existing project that extends these 
'old-style' templates.

To use these, edit your ``TEMPLATE_DIRS`` setting::


    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/old_style_templates'),
        ... other folders containing Photologue templates should come after...
    )

Fancybox
~~~~~~~~
`Fancybox <http://fancyapps.com/fancybox/>`_ is a jQuery plugin that offers a
lightbox-style zooming. You can use it on the gallery pages, and remove
the photo detail pages entirely.

1. Edit your ``TEMPLATE_DIRS`` setting::
 
    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/fancybox/templates'),
        PHOTOLOGUE_APP_DIR,
        ...
    )

2. Add to ``STATICFILES_DIRS``::

    STATICFILES_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/fancybox/static'),
    )


3. Ensure that your project provides the following:

   - jQuery is loaded.
   - The site ``base.html`` template provides a ``extra_js`` block.

4. The ``/photo/`` urls can be disabled; edit your project ``urls.py`` so that any call
   to a photo page gets redirected to the galleries view::

    from django.views.generic.base import RedirectView
    from django.core.urlresolvers import reverse_lazy

    ...
    url(r'^photologue/photo/', RedirectView.as_view(url=reverse_lazy('pl-gallery-archive'))),
    url(r'^photologue/', include('photologue.urls')),
    ...

5. If you use sitemaps, remember to only use ``GallerySitemap`` - do not use ``PhotoSitemap``. 

That's it; in practice, you will very probably want to customise Fancybox to your site,
which means that you will write your own custom templates - those provided will help
as examples.

.. note::

    * Disabling the photo views breaks the unit tests - when we're all running
      on Python 3 we'll be able to add skipTest to the concerned unit tests and
      skip them.

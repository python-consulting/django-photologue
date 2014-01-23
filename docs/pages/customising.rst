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

First, set up your template configuration as so:

.. code-block:: python

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

For example, to customise ``photologue/gallery_list.html``, you can have an implementation like:

.. code-block:: html+django

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

    Default: ``False``

If you have already installed `django-ckeditor <https://pypi.python.org/pypi/django-ckeditor>`_
then you can use to edit the TextArea fields of Gallery
and Photo in the admin. Simply set the setting to ``True``.


PHOTOLOGUE_GALLERY_PAGINATE_BY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``20``

Number of galleries to display per page for GalleryListView.


PHOTOLOGUE_PHOTO_PAGINATE_BY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``20``

Number of photos to display per page for PhotoListView.


PHOTOLOGUE_GALLERY_LATEST_LIMIT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``None``

Default limit for gallery.latest


PHOTOLOGUE_GALLERY_SAMPLE_SIZE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``5``

Number of random images from the gallery to display.


PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``100``

max_length setting for the ImageModel ImageField


PHOTOLOGUE_SAMPLE_IMAGE_PATH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``os.path.join(os.path.dirname(__file__), 'res', 'sample.jpg'))``

Path to sample image


PHOTOLOGUE_MAXBLOCK
~~~~~~~~~~~~~~~~~~~
    
    Default: ``256 * 2 ** 10``

Modify image file buffer size.


PHOTOLOGUE_DIR
~~~~~~~~~~~~~~
    
    Default: ``'photologue'``

The relative path from your ``MEDIA_ROOT`` setting where Photologue will save image files. If your ``MEDIA_ROOT`` is set to "/home/user/media", photologue will upload your images to "/home/user/media/photologue"


PHOTOLOGUE_PATH
~~~~~~~~~~~~~~~

    Default: ``None``

Look for user function to define file paths. Specifies a "callable" that takes a model instance and the original uploaded filename and returns a relative path from your ``MEDIA_ROOT`` that the file will be saved. This function can be set directly.

For example you could use the following code in a util module::

    # myapp/utils.py:

    import os 

    def get_image_path(instance, filename): 
        return os.path.join('path', 'to', 'my', 'files', filename) 

Then set in settings::

    # settings.py:

    from utils import get_image_path
    
    PHOTOLOGUE_PATH = get_image_path

Or instead, pass a string path::

    # settings.py:

    PHOTOLOGUE_PATH = 'myapp.utils.get_image_path'



Third-party contributions
-------------------------
Photologue has a 'contrib' folder that includes some
useful tweaks to the base project.

Old-style templates
~~~~~~~~~~~~~~~~~~~
Replaces the normal templates with the templates that used to come with
Photologue 2.X. Use these if you have an existing project that extends these 
'old-style' templates.

To use these, edit your ``TEMPLATE_DIRS`` setting:

.. code-block:: python

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

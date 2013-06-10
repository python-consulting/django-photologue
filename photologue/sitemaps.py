"""
Photologue can be used in your site's sitemap.xml to generate a list of all the 
Gallery and Photo pages.

To use, add the following to the sitemap definition section of your project's
urls.py::

    ...
    from photologue.sitemaps import GallerySitemap, PhotoSitemap
    
    sitemaps = {...
                'photologue_galleries': GallerySitemap,
                'photologue_photos': PhotoSitemap,
                ...
                }
    etc...

"""
import warnings

from django.contrib.sitemaps import Sitemap
from .models import Gallery, Photo

# Note: Gallery and Photo are split, because there are use cases for having galleries
# in the sitemap, but not photos (e.g. if the photos are displayed with a lightbox).

class GallerySitemap(Sitemap):
    priority = 0.5

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Gallery.objects.filter(is_public=True)

    def lastmod(self, obj):
            return obj.date_added

class PhotoSitemap(Sitemap):
    priority = 0.5

    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Photo.objects.filter(is_public=True)

    def lastmod(self, obj):
            return obj.date_added



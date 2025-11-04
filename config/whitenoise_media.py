"""
Custom WhiteNoise middleware to serve media files in production.
"""
from whitenoise.middleware import WhiteNoiseMiddleware


class WhiteNoiseMediaMiddleware(WhiteNoiseMiddleware):
    """
    Extends WhiteNoise to also serve media files from MEDIA_ROOT at MEDIA_URL.
    WhiteNoise's add_files method is called during initialization to register
    the media directory.
    """
    def __init__(self, get_response, settings=None):
        super().__init__(get_response, settings)
        from django.conf import settings as django_settings
        
        # Register media directory with WhiteNoise
        if hasattr(django_settings, 'MEDIA_ROOT') and django_settings.MEDIA_ROOT:
            media_url = django_settings.MEDIA_URL
            if media_url.endswith('/'):
                media_url = media_url[:-1]
            
            media_root = str(django_settings.MEDIA_ROOT)
            # WhiteNoise's add_files method: add_files(root, prefix='')
            self.add_files(media_root, prefix=media_url)


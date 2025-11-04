"""
Custom WhiteNoise middleware to serve media files in production.
"""
from whitenoise.middleware import WhiteNoiseMiddleware


class WhiteNoiseMediaMiddleware(WhiteNoiseMiddleware):
    """
    Extends WhiteNoise to also serve media files from MEDIA_ROOT at MEDIA_URL.
    """
    def __init__(self, application, settings=None):
        super().__init__(application, settings)
        from django.conf import settings as django_settings
        
        # Add media files directory to WhiteNoise
        if hasattr(django_settings, 'MEDIA_ROOT') and hasattr(django_settings, 'MEDIA_URL'):
            media_url = django_settings.MEDIA_URL.rstrip('/')
            media_root = str(django_settings.MEDIA_ROOT)
            self.add_files(media_root, prefix=media_url)


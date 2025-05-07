"""
WSGI config for Sigere project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import threading
from django.db import OperationalError
from django.core.wsgi import get_wsgi_application

def run_populate_script():
    try:
        from Sigere.Apps.LandingPage.models import EspacioDeportivo
        if not EspacioDeportivo.objects.exists():
            import os
            os.system("python Sigere/populate.py")
    except OperationalError:
        pass  # Base de datos aún no está lista

threading.Thread(target=run_populate_script).start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sigere.settings')

application = get_wsgi_application()

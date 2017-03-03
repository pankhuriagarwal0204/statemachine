import os
import sys

sys.path.append('/home/pankhuri-agarwal/work/analytics_api/analytics_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "analytics_api.settings")

import django
django.setup()

from django.apps import AppConfig
import os
from main.clear_task import clear_temp

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        if not os.path.exists("assets\\tmp"):
            os.makedirs("assets\\tmp")
        clear_temp()
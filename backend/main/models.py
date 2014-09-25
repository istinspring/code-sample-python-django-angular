import os

from django.conf import settings

from backend.libs.models import DynModels


DynModels(
    os.path.join(settings.BASE_DIR, 'fixtures', 'models_structure.json'),
    __name__
).create_and_register()

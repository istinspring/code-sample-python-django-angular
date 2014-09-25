import os
import json
import logging
import importlib

from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitDateWidget

from .exceptions import DynModelsException


logger = logging.getLogger('backend.libs')


class DynModels(object):
    """ Create django models dynamically using information stored in .json file

        json file format
        ================

        :: json

            {
                "model name": {
                    "field name": {
                        "type": "django field type ie. CharField, IntegerField etc.",
                        "params": { params used to create field ie. blank, null etc. }
                    }
                }
            }

    """
    def __init__(self, filepath, module):
        if not (os.path.exists(filepath) and os.path.isfile(filepath)):
            raise DynModelsException(u"Wrong filepath or not file.")
        with open(filepath, 'r') as f:
            try:
                self.models_json = json.loads(f.read())
            except ValueError:
                raise DynModelsException("Wrong json structure.")
        try:
            self.module = importlib.import_module(module)
        except ImportError:
            raise DynModelsException("Can't import module: {}".format(module))

    @staticmethod
    def module_dir_name(module):
        """ Return application directory name,
            assume that :module: located inside app directory

        """
        module_path = os.path.abspath(module.__file__)
        module_dir = os.path.dirname(module_path)
        app_directory = module_dir.split('/')[-1]
        return app_directory

    def create_and_register(self):
        """ Create model class using metaclass, and register them in
            django admin interface

        """
        # iterate all models listed in json file
        for model_name, model_data in self.models_json.items():

            class Meta:
                app_label = self.module_dir_name(self.module)
                verbose_name = model_name
                verbose_name_plural = model_name

            attrs = {
                '__module__': self.module.__name__,
                '__unicode__': lambda x: str(getattr(x, 'pk')),
                'Meta': Meta,
            }
            widgets_dict = {}  # custom widgets for django-suit

            admin_title_fields = []
            # iterate all field for model and update metaclass attributes
            for field_name, field_data in model_data['fields'].items()[::-1]:
                field_class = getattr(models, field_data['type'])
                attrs.update({field_name: field_class(**field_data['params'])})

                # define custom widgets here
                if field_data['type'] == 'DateField':
                    widgets_dict.update({field_name: SuitDateWidget})

                # check if field is for naming admin rows
                if field_data.get('admin_title', False):
                    admin_title_fields.append(field_name)

            # define custom __unicode__ method based on parsed admin_title_fields
            attrs['__unicode__'] = lambda x: " ".join(
                [str(getattr(x, fld)) for fld in admin_title_fields])

            # create model class dynamically
            model_class = type(
                str(model_name),
                (models.Model, ),
                attrs
            )
            logger.debug("{} created with attributes: {}".format(
                model_class, attrs.values()))

            class Meta:
                model = model_class
                widgets = widgets_dict

            # generate ModelForm for class
            # (used to form appropriate django-suit widget)
            admin_model_form = type(
                str(model_name) + 'ModelForm',
                (ModelForm, ),
                {'Meta': Meta}
            )

            # create admin model using generated ModelForm class
            admin_class = type(
                str(model_name) + 'Admin',
                (admin.ModelAdmin, ),
                {'form': admin_model_form},
            )

            # register our model in admin
            admin.site.register(model_class, admin_class)
            logger.debug("{} registered in admin: {}".format(
                model_class, admin_class))

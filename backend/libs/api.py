from django.db import models
from rest_framework import status
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class ModelsList(APIView):
    """ Get list of created models

    """

    restricted_models = [
        'ContentType', 'LogEntry', 'Permission',
        'Group', 'User', 'Session'
    ]

    @staticmethod
    def get_models_list():
        models_list = []
        for model in models.get_models(include_auto_created=False):
            if model.__name__ not in ModelsList.restricted_models:
                models_list.append({
                    'name': model.__name__,
                    'app': model._meta.app_label,
                })
        return models_list

    def get(self, request, format=None):
        models_list = self.get_models_list()
        return Response(models_list, status=status.HTTP_200_OK)


class ModelData(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @staticmethod
    def serializer_factory(model_class):
        class ModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = model_class

        return ModelSerializer

    @classmethod
    def get_serializer_instance(cls, model_class, *args, **kwargs):
        ModelSerializer = cls.serializer_factory(model_class)
        serializer = ModelSerializer(*args, **kwargs)
        return serializer

    def get(self, request, name=None):
        if name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_class = models.get_model('main', name)

        serializer = self.get_serializer_instance(
            model_class, model_class.objects.all(), many=True)

        return Response(
            {
                'name': name,
                'fields': [field.name for field in model_class._meta.fields],
                'types': {
                    field.name: field.__class__.__name__
                    for field in model_class._meta.fields
                },
                'data': serializer.data,
            }, status=status.HTTP_200_OK
        )

    def post(self, request, name=None):
        if name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_class = models.get_model('main', name)

        serializer = self.get_serializer_instance(
            model_class, data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None, pk=None):
        if (name is None) and (pk is None):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_class = models.get_model('main', name)

        ModelSerializer = self.serializer_factory(model_class)
        obj = model_class.objects.filter(pk=pk).first()
        serialized = ModelSerializer(request.DATA)
        if obj is not None:
            for attr, value in serialized.data.iteritems():
                setattr(obj, attr, value)
            obj.save()
            serialized_obj = ModelSerializer(obj)
            return Response(serialized_obj.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None, pk=None):
        if (name is None) and (pk is None):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model_class = models.get_model('main', name)

        obj = model_class.objects.filter(pk=pk).first()
        if obj is not None:
            obj.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

from django.db import models
from rest_framework import serializers, viewsets


class ArchitectureModel(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    content = models.CharField(max_length=1024**2, null=False, blank=False)


class ArchitectureModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchitectureModel
        fields = ('id', 'name', 'content')


class ArchitectureModelListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchitectureModel
        fields = ('id', 'name')


class ArchitectureModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArchitectureModelSerializer

    def get_queryset(self):
        queryset = ArchitectureModel.objects.all().order_by('id')
        _id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')

        if _id:
            queryset = queryset.filter(id=_id)
        elif name:
            queryset = queryset.filter(name=name).order_by('id')

        return queryset


class ArchitectureModelListViewSet(viewsets.ModelViewSet):
    serializer_class = ArchitectureModelListSerializer

    def get_queryset(self):
        queryset = ArchitectureModel.objects.all().order_by('name')

        return queryset

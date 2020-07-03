import os
import re
import yaml
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Project, ProjectType, Service, ServiceConfig, Account, Vmachine, Vmdisk, ProjectService
from .serializers import ProjectSerializer, AccountSerializer, ProjectTypeSerializer, ServiceConfigSerializer, \
    ServiceSerializer, VmachineSerializer, VmdiskSerializer, ProjectServiceSerializer
from rest_framework.decorators import action


# 项目类型
class ProjectTypeViewSet(ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = ProjectType.objects.filter(is_delete=0).all().order_by('-id')
    serializer_class = ProjectTypeSerializer
    
    @action(methods=['get','post'], detail=False, url_path='user_action')
    def user_action(self,request, *args, **kwargs):
        dd = {"w":"ww","ee":"ttt"}
        return Response(dd)

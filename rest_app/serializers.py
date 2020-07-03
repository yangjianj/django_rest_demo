from rest_framework import serializers
from .models import ProjectType, Project, ServiceConfig, Account, Service, Vmachine, Vmdisk, ProjectService


class ProjectTypeSerializer(serializers.ModelSerializer):
    """项目类型序列化器"""

    class Meta:
        model = ProjectType
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """项目信息序列化器"""

    class Meta:
        model = Project
        exclude = ('services',)


class ServiceSerializer(serializers.ModelSerializer):
    """服务信息序列化器"""

    class Meta:
        model = Service
        exclude = ('projects',)


class ProjectServiceSerializer(serializers.ModelSerializer):
    """服务信息序列化器"""

    class Meta:
        model = ProjectService
        fields = '__all__'


class ServiceConfigSerializer(serializers.ModelSerializer):
    """服务配置序列化器"""

    class Meta:
        model = ServiceConfig
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    """账号密码序列化器"""

    class Meta:
        model = Account
        fields = '__all__'


class VmdiskSerializer(serializers.ModelSerializer):
    """系统盘信息序列化器"""

    class Meta:
        model = Vmdisk
        fields = '__all__'


class VmachineSerializer(serializers.ModelSerializer):
    """虚机信息序列化器"""

    class Meta:
        model = Vmachine
        fields = (
        'id', 'vm_ID', 'vm_ip', 'vm_size', 'vm_vcore', 'vm_ram', 'vm_disc', 'vm_available', 'vm_type', 'node_name',
        'disks', 'create_time', 'vm_grafana_label', 'vm_prometheus_label')
        depth = 1

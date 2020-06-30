from datetime import datetime
from django.db import models


class ProjectType(models.Model):
    project_type = models.CharField(verbose_name='类型名称', max_length=32, unique=True, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    class Meta:
        verbose_name = u'项目类型'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        project = Project.objects.filter(project_type=self.id).all()
        for idx, item in enumerate(project):
            item.is_delete = True
            item.save()
        self.save()

    def __str__(self):
        return self.project_type


class Project(models.Model):
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, verbose_name='项目类型', max_length=32)
    project_name = models.CharField(verbose_name='中文名称', max_length=50, default='')
    project_ename = models.CharField(verbose_name='英文名称', max_length=200, default='')
    sys_version = models.CharField(verbose_name='运行版本', max_length=100, blank=True, default='')
    namespace = models.CharField(verbose_name='K8s命名空间', max_length=100, default='')
    sys_id = models.CharField(verbose_name='应用实例', max_length=100, blank=False)
    notes = models.TextField(verbose_name='备注', max_length=200, blank=True, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    creator = models.CharField(verbose_name='创建者', max_length=50, default="", blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    editor = models.CharField(verbose_name='更新人', max_length=50, default="", blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')
    services = models.ManyToManyField(to='Service', through='ProjectService', through_fields=('project', 'service'))

    class Meta:
        verbose_name = u'项目信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()
        ProjectService.objects.filter(project=self.id).delete()

    def __str__(self):
        return self.project_name


class Service(models.Model):
    service_name = models.CharField(verbose_name='服务名称', max_length=150, blank=False)
    service_cname = models.CharField(verbose_name='服务中文名称', max_length=150, default='中文名称', blank=False)
    service_port = models.IntegerField(verbose_name='服务端口', default=8000)
    protocol_type = models.CharField(verbose_name='协议类型', max_length=20)
    config_version = models.CharField(verbose_name='配置版本号', max_length=100,
                                      default=('%s' % datetime.now().strftime('%Y%m%d%H%M')))
    service_type = models.IntegerField(verbose_name='服务类型',
                                       choices=((1, 'mysql'),
                                                (2, 'mongodb'),
                                                (3, 'redis'),
                                                (4, 'others')), default=4)
    notes = models.TextField(verbose_name='备注', max_length=200, blank=True, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改日期', auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')
    projects = models.ManyToManyField(to='Project', through='ProjectService', through_fields=('service', 'project'))

    class Meta:
        verbose_name = u'服务信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        service_configs_list = ServiceConfig.objects.filter(service_name=self.id).all()
        account_configs_list = Account.objects.filter(service_name=self.id).all()
        for idx, item in enumerate(service_configs_list):
            item.is_delete = True
            item.save()
        for idx, item in enumerate(account_configs_list):
            item.is_delete = True
            item.save()
        self.save()
        ProjectService.objects.filter(service=self.id).delete()

    def __str__(self):
        return self.service_name


class ProjectService(models.Model):
    project = models.ForeignKey(to='Project', on_delete=models.PROTECT)
    service = models.ForeignKey(to='Service', on_delete=models.PROTECT)

    class Meta:
        verbose_name = u'项目服务多对多'
        verbose_name_plural = verbose_name


class ServiceConfig(models.Model):
    service_name = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='服务名称', max_length=150)
    config_type = models.IntegerField(verbose_name='配置类型',
                                    choices=((1, 'Genenral'),
                                             (2, 'ENV_VERSION')), default=1)
    config_name = models.CharField(verbose_name='配置名称', max_length=100, blank=True, default='')
    config_value = models.CharField(verbose_name='配置值', max_length=200, blank=True, default='')
    config_disc = models.CharField(verbose_name='配置说明', max_length=200, blank=True, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    class Meta:
        verbose_name = u'服务配置'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def __str__(self):
        return self.config_name


class Account(models.Model):
    service_name = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='服务名称', max_length=150)
    account_type = models.IntegerField(verbose_name='账号类型',
                                    choices=((1, 'Genenral'),
                                             (2, 'Standalone'),
                                             (3, 'ShardCluster'),
                                             (4, 'ReplicaSet')), default=1)
    account_name = models.CharField(verbose_name='帐号名称', max_length=100, default='')
    account_password = models.CharField(verbose_name='账号密码', max_length=100, default='')
    account_level = models.IntegerField(verbose_name='账号等级',
                                    choices=((1, '管理员用账号'),
                                             (2, '使用者账号')), default=1)
    db_name = models.CharField(verbose_name='数据库名称', max_length=100, default='')
    auth_db = models.CharField(verbose_name='MongoAdmin_DB', max_length=100, default='')
    notes = models.TextField(verbose_name='备注', max_length=200, blank=True, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    class Meta:
        verbose_name = u'账密配置'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def __str__(self):
        return self.account_name


class Vmachine(models.Model):
    vm_ID = models.CharField(verbose_name='虚机ID', max_length=100, blank=False, default='')
    vm_ip = models.CharField(verbose_name='虚机IP', max_length=20, default='0.0.0.0')
    vm_vcore = models.IntegerField(verbose_name='虚机核数', default=1)
    vm_ram = models.IntegerField(verbose_name='虚机内存/G', default=4)
    vm_size = models.IntegerField(verbose_name='系统盘大小/G', blank=False, default=1)
    vm_disc = models.CharField(verbose_name='虚机描述', max_length=200, default='')
    vm_available = models.IntegerField(verbose_name='使用情况', choices=(
        (1, '使用中'),
        (0, '空闲中'),
    ), default=0)
    vm_type = models.IntegerField(verbose_name='虚机类型', choices=(
        (1, 'controller'),
        (0, 'working'),
    ), default=0)
    node_name = models.CharField(verbose_name='工作节点', max_length=200, default='')
    vm_grafana_label = models.CharField(verbose_name='G标签', max_length=200, default='')
    vm_prometheus_label = models.CharField(verbose_name='P标签', max_length=200, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        vmdisk = Vmdisk.objects.filter(vm=self.id).all()
        for idx, item in enumerate(vmdisk):
            item.is_delete = True
            item.save()
        self.save()

    def vm_storage(self):
        return Vmdisk.objects.filter(vm__vm_ip=self.vm_ip).count()

    vm_storage.short_description = '数据盘数目'

    class Meta:
        verbose_name = u'虚机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.vm_ip


class Vmdisk(models.Model):
    vm = models.ForeignKey(Vmachine, verbose_name="绑定的虚机", on_delete=models.CASCADE, related_name='disks')
    disk_name = models.CharField(verbose_name="数据盘的名称", max_length=50, blank=False)
    disk_size = models.IntegerField(verbose_name="数据盘的大小", blank=False)
    disk_disc = models.CharField(verbose_name="数据盘的用途说明", max_length=200, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    class Meta:
        verbose_name = '数据盘信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def __str__(self):
        return self.disk_name

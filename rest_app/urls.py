from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'app1'
router = DefaultRouter()  # 可以处理视图的路由器

router.register(r'projects', views.ProjectTypeViewSet)
#router.register(r'user_action', views.ProjectTypeViewSet.as_view({'get':'user_action'}))


urlpatterns = [
    # 导出功能的url
    #url(r'^configyml/$', views.configYml),
]
urlpatterns += router.urls

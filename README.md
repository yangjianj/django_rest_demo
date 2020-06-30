## django_rest_framework框架练习项目  
# django_rest_demo
rest_framework demo  
## app说明  
normal_app普通  
rest_app使用restframework

## 简要笔记    
1.序列化类：serializers.ModelSerializer 跟模型紧密相关的序列化器。    
快速创建对应模型的序列化类    


2.视图类：ModelViewSet 继承自 GenericAPIView < APIView < View
必须定义类属性(在GenericAPIView定义，常用方法会用到此属性：self.get_queryset;self.get_object;self.get_serializer ..等) 
queryset = User.objects.all() #该类操作的
serializer_class = CreateUserSerializer #该类的序列化类
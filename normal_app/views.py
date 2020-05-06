from django.shortcuts import render
import json
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
# Create your views here.

class CourseView(View):
	def get(self,request):
		data = '{"a":1}'
		json_data = json.loads(data)
		return JsonResponse(json_data)
	
	def post(self,request):
		data = '{"a":1}'
		json_data = json.loads(data)
		return JsonResponse(json_data)

	def put(self,request):
		data = '{"a":1}'
		json_data = json.loads(data)
		return JsonResponse(json_data)

	def delete(self,request):
		data = '{"a":1}'
		json_data = json.loads(data)
		return JsonResponse(json_data)
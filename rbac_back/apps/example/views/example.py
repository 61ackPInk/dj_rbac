"""
-*- coding: utf-8 -*-
@File  : example.py
@Author: 61ackPink
@Time : 2026/9/10 14:58
@Desc : 示例：视图
"""
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.example.serializers.example import ExampleSerializer


class ExampleAPIView(GenericAPIView):

    def get(self, request):
        return Response('示例app!')
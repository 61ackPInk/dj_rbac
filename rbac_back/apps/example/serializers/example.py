"""
-*- coding: utf-8 -*-
@File  : example.py
@Author: 61ackPink
@Time : 2026/9/10 14:58
@Desc : 示例：序列化文件
"""
from rest_framework import serializers
from apps.example.models import Example

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'

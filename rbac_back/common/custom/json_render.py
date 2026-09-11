"""
-*- coding: utf-8 -*-
@File  : json_render.py
@Author: 61ackPink
@Time : 2026/9/10 15:12
@Desc : 重新JsonResponse
"""
from rest_framework.renderers import JSONRenderer

class Renderer(JSONRenderer):
    """重写Json渲染器"""
    def render(self, data ,media_type=None, renderer_context=None):
        if renderer_context:
            # 自定义返回
            response = {
                'code': renderer_context['response'].status_code,
                'message': 'success',
                'data': data
            }
            # 返回json格式
            return super().render(response, media_type, renderer_context)
        else:
            return super().render(data, media_type, renderer_context)
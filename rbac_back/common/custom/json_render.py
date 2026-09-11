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
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 没有响应上下文时，使用 DRF 默认处理
        if not renderer_context:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )
        response = renderer_context["response"]
        status_code = response.status_code
        is_success = status_code < 400
        if is_success:
            result = {
                "code": status_code,
                "message": "success",
                "data": data,
            }
        else:
            result = {
                "code": status_code,
                "message": "error",
                "data": None,
                "errors": data,
            }

        return super().render(
            result,
            accepted_media_type,
            renderer_context,
        )


    # def render(self, data ,media_type=None, renderer_context=None):
    #     if renderer_context:
    #         # 自定义返回
    #         response = {
    #             'code': renderer_context['response'].status_code,
    #             'message': 'success',
    #             'data': data
    #         }
    #         # 返回json格式
    #         return super().render(response, media_type, renderer_context)
    #     else:
    #         return super().render(data, media_type, renderer_context)
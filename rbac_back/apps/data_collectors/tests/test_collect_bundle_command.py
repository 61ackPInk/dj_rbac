"""
-*- coding: utf-8 -*-
@File  : test_collect_bundle_command.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 元仓组合映射采集命令测试
"""

from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import (
    call_command,
)
from django.core.management.base import (
    CommandError,
)
from django.test import SimpleTestCase

from apps.data_collectors.collectors.exceptions import (
    CollectorRequestError,
)


COMMAND_CLASS_PATH = (
    "apps.data_collectors.management.commands."
    "collect_yuancang_bundle_mappings."
    "Command.build_service"
)


class CollectBundleCommandTests(
    SimpleTestCase
):
    """元仓组合映射采集命令测试。"""

    @patch(COMMAND_CLASS_PATH)
    def test_command_outputs_success_result(
        self,
        build_service,
    ):
        """采集成功时输出数量统计。"""

        service = Mock()
        service.run.return_value = {
            "total": 12,
            "created": 10,
            "updated": 2,
            "deactivated": 3,
            "failed": 0,
            "errors": [],
        }
        build_service.return_value = service

        output = StringIO()

        call_command(
            "collect_yuancang_bundle_mappings",
            stdout=output,
        )

        output_value = output.getvalue()

        self.assertIn(
            "总数 12",
            output_value,
        )
        self.assertIn(
            "新增 10",
            output_value,
        )
        self.assertIn(
            "更新 2",
            output_value,
        )
        self.assertIn(
            "失效 3",
            output_value,
        )
        self.assertIn(
            "元仓组合映射采集完成",
            output_value,
        )

    @patch(COMMAND_CLASS_PATH)
    def test_command_converts_collector_error(
        self,
        build_service,
    ):
        """采集异常会转换为命令错误。"""

        service = Mock()
        service.run.side_effect = (
            CollectorRequestError(
                "无法连接元仓"
            )
        )
        build_service.return_value = service

        with self.assertRaisesRegex(
            CommandError,
            "组合映射采集失败",
        ):
            call_command(
                "collect_yuancang_bundle_mappings"
            )

    @patch(COMMAND_CLASS_PATH)
    def test_command_reports_save_failure(
        self,
        build_service,
    ):
        """部分保存失败时命令返回错误。"""

        service = Mock()
        service.run.return_value = {
            "total": 2,
            "created": 1,
            "updated": 0,
            "deactivated": 0,
            "failed": 1,
            "errors": [
                {
                    "bundle_sku": (
                        "BUNDLE-002"
                    ),
                    "message": (
                        "模拟数据库错误"
                    ),
                }
            ],
        }
        build_service.return_value = service

        output = StringIO()
        error_output = StringIO()

        with self.assertRaisesRegex(
            CommandError,
            "部分组合映射保存失败",
        ):
            call_command(
                "collect_yuancang_bundle_mappings",
                stdout=output,
                stderr=error_output,
            )

        self.assertIn(
            "BUNDLE-002",
            error_output.getvalue(),
        )
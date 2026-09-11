"""
-*- coding: utf-8 -*-
@File  : config.py
@Author: 61ackPink
@Time : 2026/8/25 16:01
@Desc : 日志框架配置文件
"""

import os
from pathlib import Path

# ==================== 控制台日志配置 ====================

LOG_CONSOLE = {
    # 控制台输出（TRUE=启用。FALSE=禁用）
    "enable": True,
    # 日志输出的最低级别
    # 可选值: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR < CRITICAL
    # INFO 级别会输出 INFO、SUCCESS、WARNING、ERROR、CRITICAL
    # 不输出 TRACE 和 DEBUG
    "level": "INFO",
    # 控制台输出格式
    "format": (
        "{extra[icon]} "
        "<level>{level:<7}</level> | "
        "<green>{time:HH:mm:ss}</green> | "
        "<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"  # ← {file} 只显示文件名
        "         └─ <level>{message}</level>"
    )
}

# ==================== 文件日志配置 ====================
LOG_FILE = {
    # 是否保存日志到文件
    "enable": True,
    # 保存的最低级别
    "level": "ERROR",
    # 文件保存路径 及 格式
    "path": "logs/app_{time:YYYY-MM-DD}.log",
    # 日志轮转策略：文件到达10MB时，创建新文件
    "rotation": "10 MB",
    # 日志保留策略：保留30天
    "retention": "30 days",
    # 旧日志文件压缩格式（zip）
    "compression": "zip",
    # 文件自定义格式
    "format": (
        "[{time:YYYY-MM-DD HH:mm:ss.SSS}] "
        "[{level:<8}] "
        "[{name}:{function}:{line}] "
        "[PID:{process} TID:{thread}] "  # ← 添加 PID 和 TID，便于多进程调试
        "{message}"
    )
}

# ==================== # 图标配置 # ====================
ICONS = {
    "TRACE": "🔍",
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "SUCCESS": "✅",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "💀",
}

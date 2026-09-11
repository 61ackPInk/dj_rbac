"""
-*- coding: utf-8 -*-
@File  : log.py
@Author: 61ackPink
@Time : 2026/8/25 16:01
@Desc : 日志核心文件
"""

import sys
import signal
import atexit
from pathlib import Path
from loguru import logger
from common.utils.log import config as log_config

class LogConfig:
    """
    日志配置类
    """
    def __init__(self):
        """
        构造函数
        读取配置
        """
        # 控制台配置
        self.console_enable = log_config.LOG_CONSOLE.get("enable")
        self.console_level = log_config.LOG_CONSOLE.get("level")
        self.console_format = log_config.LOG_CONSOLE.get("format")

        # 文件配置
        self.file_enable = log_config.LOG_FILE.get("enable")
        self.file_level = log_config.LOG_FILE.get("level")
        self.file_path = log_config.LOG_FILE.get("path")
        self.file_rotation = log_config.LOG_FILE.get("rotation")
        self.file_retention = log_config.LOG_FILE.get("retention")
        self.file_compression = log_config.LOG_FILE.get("compression")
        self.file_format = log_config.LOG_FILE.get("format")

        # 图标配置
        self.icons = log_config.ICONS

        # 计算项目根目录
        self.project_root = self.find_project_root()
        # 构建日志文件路径
        if not Path(self.file_path).is_absolute():
            # 如果是相对路径,需要和根目录进行拼接
            self.full_log_path = self.project_root / self.file_path
        else:
            # 如果是绝对路径,直接使用
            self.full_log_path = Path(self.file_path)

        # ---- 确保日志目录存在 ----
        log_dir = self.full_log_path.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建日志目录: {log_dir}")

        # ---- 注册程序退出清理 ----
        self._register_cleanup()

    @staticmethod
    def find_project_root() -> Path:
        """查找项目根目录"""
        current = Path(__file__).resolve()

        # 方案一: 查找包含django项目标志文件: manage.py
        for parent in current.parents:
            if (parent / "manage.py").exists():
                return parent

        # 方案二：其他常见标志
        for parent in current.parents:
            if (parent / ".git").exists() or (parent / "requirements.txt").exists():
                return parent

        # 方案三: 降级方案
        return current.parent.parent.parent.parent

    def _register_cleanup(self):
        """
        注册程序退出时的清理函数
        释放日志文件句柄，便于删除日志文件
        """
        # 1. 正常退出时清理
        atexit.register(self._cleanup_logger)

        # 2. 捕获 Ctrl+C 信号
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except (ValueError, AttributeError):
            # 在某些环境下可能无法设置信号处理器
            pass

        # 3. Windows 特殊处理
        if sys.platform == "win32":
            try:
                signal.signal(signal.SIGBREAK, self._signal_handler)
            except (ValueError, AttributeError):
                pass

    def _signal_handler(self, signum, frame):
        """信号处理器：处理 Ctrl+C 等信号"""
        print(f"\n📢 收到退出信号 ({signum})，正在清理日志资源...")
        self._cleanup_logger()
        sys.exit(0)

    def _cleanup_logger(self):
        """
        清理日志资源，释放文件句柄
        程序退出后即可删除日志文件
        """
        try:
            # 刷新所有待写入的日志
            logger.complete()
            # 移除所有处理器，释放文件句柄
            logger.remove()
            print("✅ 日志资源已释放，可以安全删除日志文件")
        except Exception as e:
            print(f"⚠️ 清理日志资源时出错: {e}")

    def setup(self):
        """
        配置日志系统
        """
        # 清除默认
        logger.remove()

        # 配置控制台
        if self.console_enable:
            logger.add(
                sink=sys.stdout,
                level=self.console_level,
                format=self.console_format,
                colorize=True,
                enqueue=True,  # 异步输出，提升性能
                backtrace=True,  # 显示完整堆栈
                diagnose=True,  # 显示变量值（开发环境）
                catch=True,  # 捕获处理器异常
            )

        # 配置文件
        if self.file_enable:
            logger.add(
                sink=str(self.full_log_path),
                level=self.file_level,
                format=self.file_format,
                rotation=self.file_rotation,
                retention=self.file_retention,
                compression=self.file_compression,
                encoding="utf-8",
                enqueue=True,
                backtrace=True,
                diagnose=False,
                catch=True,
            )

        # 配置异常捕获
        self._setup_exception_handler()

        return logger

    def _setup_exception_handler(self):
        """
        配置全局异常捕获
        捕获未被try...except处理的异常
        """
        # 保存系统的默认异常处理器
        default_handler = sys.excepthook

        def handle_exception(exc_type, exc_value, exc_traceback):
            """
            自定义异常处理函数
            """
            # 如果是用户按 Ctrl+C，不拦截
            if issubclass(exc_type, KeyboardInterrupt):
                default_handler(exc_type, exc_value, exc_traceback)
                return

            try:
                # 获取 CRITICAL 级别的图标
                icon = self.get_icon("CRITICAL")
                # 记录异常到日志
                logger.bind(icon=icon).opt(
                    exception=(exc_type, exc_value, exc_traceback)
                ).critical(
                    f"程序发生未捕获异常: {exc_type.__name__}: {exc_value}"
                )
            except Exception:
                # 如果日志系统出错，降级到默认处理
                default_handler(exc_type, exc_value, exc_traceback)

        # 替换系统的异常处理器
        sys.excepthook = handle_exception

    def get_icon(self, level: str) -> str:
        """
        获取指定级别的图标
        """
        return self.icons.get(level.upper(), "")

class LoguruLogger:
    """
    日志类封装
    """
    def __init__(self, config: LogConfig):
        """
        构造函数
        config: LogConfig
        """
        self._config = config
        self._logger = logger

        # 原始方法
        self._original = {
            "trace": logger.trace,
            "debug": logger.debug,
            "info": logger.info,
            "success": logger.success,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical,
            "exception": logger.exception,
        }

        # 注入图标
        self._inject_icons()

    def _inject_icons(self):
        """
        注入图标到所有日志方法
        """
        levels = ["trace", "debug", "info", "success", "warning", "error", "critical"]
        for level in levels:
            original = self._original[level]
            setattr(self._logger, level, self._make_icon_method(original, level.upper()))

        # exception 使用 ERROR 图标
        self._logger.exception = self._make_icon_method(
            self._original["exception"],
            "ERROR"
        )

    def _make_icon_method(self, original_method, level: str):
        """
        创建带图标的方法
        """
        def wrapper(message, *args, **kwargs):
            icon = self._config.get_icon(level)
            # 使用 __getattribute__ 避免递归调用
            self._logger.bind(icon=icon).__getattribute__(original_method.__name__)(
                message, *args, **kwargs
            )
        return wrapper

    # ==================== 扩展方法 ====================

    def separator(self, char: str = "=", length: int = 80, level: str = "INFO") -> None:
        """
        打印分隔线

        Args:
            char: 分隔线使用的字符
            length: 分隔线长度
            level: 日志级别
        """
        line = char * length
        icon = self._config.get_icon(level)
        self._logger.bind(icon=icon).log(level.upper(), line)

    def with_context(self, **kwargs):
        """
        绑定上下文信息

        Args:
            **kwargs: 键值对，如 user_id=1001, ip="192.168.1.1"

        Returns:
            logger: 绑定了上下文的 logger 对象
        """
        return self._logger.bind(**kwargs)

    # ==================== 兼容 Loguru 原生方法 ====================

    def __getattr__(self, name):
        """
        转发未定义的方法到原始 logger
        保证所有 Loguru 原生方法可用
        """
        if hasattr(self._logger, name):
            return getattr(self._logger, name)
        raise AttributeError(f"'{self.__class__.__name__}' 没有属性 '{name}'")

    # ==================== 属性 ====================

    @property
    def config(self) -> LogConfig:
        """获取配置对象（只读）"""
        return self._config


# ==================== 初始化 ====================

# 创建配置实例
config = LogConfig()

# 配置日志系统
config.setup()

# 创建带图标的日志对象
log = LoguruLogger(config)


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 日志系统测试")
    print("=" * 70 + "\n")

    # 测试所有日志级别
    print("📋 测试各级别日志：")
    print("-" * 70)
    log.trace("🔍 TRACE 级别")
    log.debug("🐛 DEBUG 级别")
    log.info("ℹ️ INFO 级别")
    log.success("✅ SUCCESS 级别")
    log.warning("⚠️ WARNING 级别")
    log.error("❌ ERROR 级别")
    log.critical("💀 CRITICAL 级别")

    print("\n" + "-" * 70)
    print("📋 测试格式化输出：")
    print("-" * 70)
    log.info("用户 {} 登录成功，ID: {}", "张三", 1001)
    log.info("用户信息: {user}", user={"name": "李四", "age": 25})

    print("\n" + "-" * 70)
    print("📋 测试分隔线：")
    print("-" * 70)
    log.separator("=", 60, "INFO")
    log.info("开始批量处理任务...")
    log.separator("-", 60, "INFO")

    print("\n" + "-" * 70)
    print("📋 测试上下文绑定：")
    print("-" * 70)
    user_log = log.with_context(user_id=1001, ip="192.168.1.100")
    user_log.info("用户查询数据")
    user_log.info("用户导出报告")

    print("\n" + "-" * 70)
    print("📋 测试异常捕获：")
    print("-" * 70)
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("捕获到除零异常")

    print("\n" + "=" * 70)
    print("✅ 日志测试完成！")
    print(f"📁 日志文件位置: {config.full_log_path}")
    print("=" * 70)
class BizException(Exception):
    """自定义业务异常类，包含错误码和错误信息"""

    def __init__(self, code: int, message: str):
        """初始化异常对象

        Args:
            code: 错误码
            message: 错误信息
        """
        self.code = code
        self.message = message
        super().__init__(message)
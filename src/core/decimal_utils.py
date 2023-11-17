from decimal import Decimal, ROUND_HALF_UP


class DecimalUtils:

    @staticmethod
    def round(number: str, precision: int = 0):
        """
        自定义浮点型四舍五入
        :param number: 输入数值
        :param precision: 浮点型的精度位数, 可能是负数
        :return:
        """
        number_decimal = Decimal(number)
        number_float = float(number)

        sign = 1  # 正负号处理， 默认是正号
        if number_decimal < 0:  # 符号变更 (Decimal 的 quantize 不支持负数, 需要先转为正数)
            sign = -1
            number_float = number_float * -1

        if precision <= 0:
            # 整数或者负精度的数字的处理方式
            base = 10 ** precision
            big = number_float * base + 0.5  # 先变小'精度*10'倍, 然后 +0.5 进位
            restore = int(big) / base
            return sign * restore

        precision = str(1 / 10 ** precision)
        return number_decimal.quantize(Decimal(precision), rounding=ROUND_HALF_UP) * sign

    @staticmethod
    def sum(*args: str):
        res = Decimal(0)
        for arg in args:
            res += Decimal(arg)
        return str(res)

    @staticmethod
    def sub(num1: str, num2: str):
        res = Decimal(num1) - Decimal(num2)
        return str(res)

    @staticmethod
    def mul(*args: str):
        res = Decimal(1)
        for arg in args:
            res *= Decimal(arg)
        return str(res)

    @staticmethod
    def div(num1: str, num2: str):
        res = Decimal(num1) / Decimal(num2)
        return str(res)

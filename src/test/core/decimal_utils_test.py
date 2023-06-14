from core.base_class import Core
from core.decimal_utils import DecimalUtils


def test_decimal_round():
    core.logger.info("********************************* test_decimal_round *********************************")
    core.logger.info(f"normal round: {round(3.14159265358979323846, 19)} \tcustom round:{DecimalUtils.round('3.14159265358979323846', 19)}")
    core.logger.info(f"normal round: {round(-6.25, -1)} \tcustom round:{DecimalUtils.round('-6.25', -1)}")
    core.logger.info(f"normal round: {round(6.25, -2)}\tcustom round:{DecimalUtils.round('6.25', -2)}")


def test_decimal_sum():
    core.logger.info("********************************* test_decimal_add *********************************")
    core.logger.info(f"normal add: {0.1 + 0.2 - 0.3} \tcustom add:{DecimalUtils.sum('0.1', '0.2', '-0.3')}")


def test_decimal_sub():
    core.logger.info("********************************* test_decimal_sub *********************************")
    core.logger.info(f"normal sub: {0.3 - 0.2} \tcustom sub:{DecimalUtils.sub('0.3', '0.2')}")


def test_decimal_mul():
    core.logger.info("********************************* test_decimal_mul *********************************")
    core.logger.info(f"normal mul: {0.1 * 3 * 5} \tcustom mul:{DecimalUtils.mul('0.1', '3', '5')}")


def test_decimal_div():
    core.logger.info("********************************* test_decimal_div *********************************")
    core.logger.info(f"normal div: {1 / 3} \tcustom div:{DecimalUtils.div('1', '3')}")


if __name__ == "__main__":
    core = Core()
    core.init("dev")

    test_decimal_round()

    test_decimal_sum()
    test_decimal_sub()
    test_decimal_mul()
    test_decimal_div()

    res = DecimalUtils.sum('1000000000000000000', '2', '3')
    core.logger.info(res)

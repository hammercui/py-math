import time
from core.base_class import Core, Async


@Async
def test_async():
    logger.info("start call")
    time.sleep(1)
    logger.info("end call")


if __name__ == "__main__":
    core = Core()
    core.init(env="dev")
    logger = core.logger

    test_async()
    test_async()
    test_async()

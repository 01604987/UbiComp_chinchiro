from lib import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("test msg")

class CustomHandler(logging.Handler):
    def emit(self, record):
        print("levelname=%(levelname)s name=%(name)s message=%(message)s" % record.__dict__)

logger.addHandler(CustomHandler())
logger.info("Test")
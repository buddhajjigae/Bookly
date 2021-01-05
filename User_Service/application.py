from user_svc.log import logger
from user_svc.app import application

logger.debug("__name__ = " + str(__name__))

if __name__ == "__main__":
    # For local Testing
    application.run(port=8000)

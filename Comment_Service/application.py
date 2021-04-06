from comment_svc.log import logger
from comment_svc.app import application

logger.debug("__name__ = " + str(__name__))

if __name__ == "__main__":
    # For local Testing
    application.run(port=8000)

    # For ECS deployment
    # application.run(host="0.0.0.0", port=80)

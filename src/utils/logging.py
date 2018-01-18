import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)8s] %(asctime)s : %(message)s'
)

logger = logging.getLogger(__name__)

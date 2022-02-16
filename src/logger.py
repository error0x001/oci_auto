import logging
import sys


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s - %(message)s",
        handlers=[logging.FileHandler("oci.log"), logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(__name__)


logger = get_logger()

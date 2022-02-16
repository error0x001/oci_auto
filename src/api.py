from typing import Tuple

from oci.exceptions import ServiceError

from logger import logger
from oci_client import oci_client


def is_succeed_preparation() -> Tuple[bool, str]:
    try:
        oci_client.prepare_client()
        if not oci_client.has_available_instance():
            msg = "check your config and your existing instances"
            logger.error(msg)
            return False, msg
        msg = "client is prepared"
        logger.info(msg)
        return True, msg
    except Exception as exc:
        msg = f"failed to prepare client, error {exc}"
        logger.error(msg)
        return False, msg


def is_instance_launched() -> bool:
    try:
        oci_client.launch()
        return True
    except ServiceError as exc:
        logger.info(f"{exc.message} - retry in {oci_client.wait_interval}s")
        return False
    except Exception as exc:
        logger.error(f"excepted error: {exc}")
        return False

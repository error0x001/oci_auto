from oci.exceptions import ServiceError

from logger import logger
from oci_client import oci_client


def is_succeed_preparation() -> str:
    try:
        oci_client.prepare_client()
        oci_client.has_available_instance()
        msg = "client is prepared"
        logger.info(msg)
        return msg
    except Exception as exc:
        msg = f"failed to prepare client, error {exc}"
        logger.error(msg)
        raise exc


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

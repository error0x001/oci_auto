import os
from dataclasses import dataclass


@dataclass
class Config:
    ocpus: int
    memory_in_gbs: int
    wait_interval: int
    instance_display_name: str
    compartment_id: str
    domain: str
    image_id: str
    subnet_id: str
    ssh_key: str
    path_to_config_file: str

    bot_id: str
    chat_id: str


config = Config(
    ocpus=int(os.getenv("OCPUS")),
    memory_in_gbs=int(os.getenv("MEMORY_IN_GBS")),
    wait_interval=int(os.getenv("WAIT_INTERVAL")),
    instance_display_name=os.getenv("INSTANCE_DISPLAY_NAME"),
    compartment_id=os.getenv("COMPARTMENT_ID"),
    domain=os.getenv("DOMAIN"),
    image_id=os.getenv("IMAGE_ID"),
    subnet_id=os.getenv("SUBNET_ID"),
    ssh_key=os.getenv("SSH_KEY"),
    path_to_config_file=os.getenv("PATH_TO_CONFIG_FILE"),
    bot_id=os.getenv("BOT_ID"),
    chat_id=os.getenv("CHAT_ID"),
)

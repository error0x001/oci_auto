from dataclasses import dataclass
from typing import Optional, Any, Dict, List

from oci import Response
from oci.core import ComputeClient
import oci
from oci.core.models import LaunchInstanceDetails

from config import config


@dataclass
class Instance:
    name: str
    ram: int
    ocpus: int


class OCI:
    __SHAPE_A1_FLEX = "VM.Standard.A1.Flex"
    __TERMINATED_STATUSES = ("TERMINATING", "TERMINATED")
    __MAX_OCPUS = 4
    __MAX_RAM = 24

    def __init__(
        self,
        ocpus: int,
        memory_in_gbs: int,
        wait_interval: int,
        instance_display_name: str,
        compartment_id: str,
        domain: str,
        image_id: str,
        subnet_id: str,
        ssh_key: str,
        path_to_config_file: str,
    ) -> None:
        self.__client: Optional[ComputeClient] = None
        self.__config: Optional[Dict[Any, Any]] = None
        self.__instances: Optional[Response] = None
        self.__launch_request: Optional[LaunchInstanceDetails] = None

        self.ocpus = ocpus
        self.memory_in_gbs = memory_in_gbs
        self.wait_interval = wait_interval
        self.instance_display_name = instance_display_name
        self.compartment_id = compartment_id
        self.domain = domain
        self.image_id = image_id
        self.subnet_id = subnet_id
        self.ssh_key = ssh_key
        self.path_to_config_file = path_to_config_file

    def __prepare_config(self) -> None:
        self.__config = oci.config.from_file(file_location=self.path_to_config_file)

    def __prepare_client(self) -> None:
        self.__client = ComputeClient(self.__config)

    def __prepare_instance(self) -> None:
        self.__instances = self.__client.list_instances(
            compartment_id=self.compartment_id
        )

    def __prepare_launch_request(self) -> None:
        self.__launch_request = LaunchInstanceDetails(
            metadata={"ssh_authorized_keys": self.ssh_key},
            availability_domain=self.domain,
            shape=self.__SHAPE_A1_FLEX,
            compartment_id=self.compartment_id,
            display_name=self.instance_display_name,
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image", image_id=self.image_id
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=False,
                subnet_id=self.subnet_id,
                assign_private_dns_record=True,
            ),
            agent_config=oci.core.models.LaunchInstanceAgentConfigDetails(
                is_monitoring_disabled=False,
                is_management_disabled=False,
                plugins_config=[
                    oci.core.models.InstanceAgentPluginConfigDetails(
                        name="Vulnerability Scanning", desired_state="DISABLED"
                    ),
                    oci.core.models.InstanceAgentPluginConfigDetails(
                        name="Compute Instance Monitoring", desired_state="ENABLED"
                    ),
                    oci.core.models.InstanceAgentPluginConfigDetails(
                        name="Bastion", desired_state="DISABLED"
                    ),
                ],
            ),
            defined_tags={},
            freeform_tags={},
            instance_options=oci.core.models.InstanceOptions(
                are_legacy_imds_endpoints_disabled=False
            ),
            availability_config=oci.core.models.LaunchInstanceAvailabilityConfigDetails(
                recovery_action="RESTORE_INSTANCE"
            ),
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=self.ocpus, memory_in_gbs=self.memory_in_gbs
            ),
        )

    def get_instances(self) -> List[Instance]:
        instances = []
        if not self.__instances.data:
            return instances

        for instance in self.__instances.data:
            if (
                instance.shape != self.__SHAPE_A1_FLEX
                or instance.lifecycle_state in self.__TERMINATED_STATUSES
            ):
                continue
            instances.append(
                Instance(
                    name=instance.display_name,
                    ocpus=int(instance.shape_config.ocpus),
                    ram=int(instance.shape_config.memory_in_gbs),
                )
            )
        return instances

    def prepare_client(self) -> None:
        self.__prepare_config()
        self.__prepare_client()
        self.__prepare_instance()
        self.__prepare_launch_request()

    def has_available_instance(self) -> bool:
        used_ram = 0
        used_ocpuc = 0
        for i in self.get_instances():
            if self.instance_display_name == i.name:
                return False
            used_ram += i.ram
            used_ocpuc += i.ocpus
        return used_ram <= self.__MAX_RAM and used_ocpuc <= self.__MAX_OCPUS

    def launch(self) -> None:
        self.__client.launch_instance(self.__launch_request)


oci_client = OCI(
    ocpus=config.ocpus,
    memory_in_gbs=config.memory_in_gbs,
    wait_interval=config.wait_interval,
    instance_display_name=config.instance_display_name,
    compartment_id=config.compartment_id,
    domain=config.domain,
    image_id=config.image_id,
    subnet_id=config.subnet_id,
    ssh_key=config.ssh_key,
    path_to_config_file=config.path_to_config_file,
)

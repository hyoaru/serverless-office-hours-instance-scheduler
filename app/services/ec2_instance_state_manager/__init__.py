from typing import Any, Dict, List, Literal

from botocore.client import BaseClient

from app.services.ec2_instance_state_manager.interface import Ec2InstanceStateManagerABC
from app.services.ec2_instance_state_manager.strategies.factory import Ec2InstanceStateManagerStrategyFactory

__all__ = ["Ec2InstanceStateManager", "Ec2InstanceStateManagerABC"]


class Ec2InstanceStateManager(Ec2InstanceStateManagerABC):
    client: BaseClient
    filters: List[Dict[str, Any]]

    def __init__(
        self,
        client: BaseClient,
        environment: Literal["dev", "stage", "prod"],
    ):
        self.client = client
        self.filters = [
            {"Name": "tag:Environment", "Values": [environment]},
            {"Name": "tag:Schedule", "Values": ["office-hours"]},
        ]

    def execute(self, strategy: str):
        return Ec2InstanceStateManagerStrategyFactory.create(strategy).execute(self)

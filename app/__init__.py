import json
import os
from typing import Literal, cast

import boto3
from dotenv import load_dotenv

from app.services.ec2_instance_state_manager import Ec2InstanceStateManager
from app.utilities.logger import Logger

load_dotenv()

ec2 = boto3.client("ec2")


def handler(event, context):
    Logger.setup_logging(is_verbose=True)
    logger = Logger.get_instance()

    logger.info("Initializing parameters")
    environment = cast(Literal["dev", "stage", "prod"], os.environ["ENVIRONMENT"])
    action = event["action"]

    logger.info(f"Executing {action} for environment: {environment}")
    Ec2InstanceStateManager(ec2, environment).execute(action)

    return json.dumps({"status": 200, "message": f"Successfully executed {action}"})

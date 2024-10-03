from flask import Blueprint, jsonify
from jenkins import JenkinsException
import logging
from time import sleep

from jenkins_api import server, wait_for_build_to_start, PIPELINE_NAME

routes_bp = Blueprint('routes_bp', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@routes_bp.route('/trigger-build', methods=['POST'])
def trigger_build():
    res: dict = {"status": None, "body": None}

    # Trigger the build
    try:
        queue_item = server.build_job(PIPELINE_NAME)
        build_number = wait_for_build_to_start(server, queue_item, PIPELINE_NAME)
    except JenkinsException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Error triggering build: {str(e)}"
        return jsonify(res), 500
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        return jsonify(res), 500

    # Construct response
    build_url = f"{server.server}job/{PIPELINE_NAME}/{build_number}"
    res["status"] = "success"
    res["info"] = {"build_number": build_number, "build_url": build_url, "name": PIPELINE_NAME}

    # Log successfull build trigger
    logger.info(f"Build triggered for pipeline: {PIPELINE_NAME}, Build number: {build_number}")

    return jsonify(res), 200

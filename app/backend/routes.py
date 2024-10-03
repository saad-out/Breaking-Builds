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
    res: dict = {"status": -1, "body": {}}

    # Trigger the build
    try:
        queue_item = server.build_job(PIPELINE_NAME)
    except JenkinsException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Error triggering build: {str(e)}"
        return jsonify(res), 500
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        return jsonify(res), 500

    # Construct response
    res["status"] = "success"
    res["body"]["info"] = {"queue_id": queue_item, "name": PIPELINE_NAME}

    # Log successfull build trigger
    logger.info(f"Build triggered for pipeline: {PIPELINE_NAME}, Build queue id: {queue_item}")

    return jsonify(res), 202

@routes_bp.route('/queue-state/<int:build_id>', methods=['GET'])
def get_build_queue_state(build_id: int):
    res: dict = {"status": -1, "body": {}}

    # Get the build queue state
    try:
        queue_info = server.get_queue_item(build_id)
    except JenkinsException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Error getting build queue state: {str(e)}"
        return jsonify(res), 500
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        return jsonify(res), 500
    
    # Construct response
    state = ''
    if 'executable' in queue_info:
        state = 'left'
    elif queue_info.get('cancelled', False) == True:
        state = 'cancelled'
    else:
        state = 'queued'
    res["status"] = "success"
    res["body"]["state"] = state

    # Log build state
    logger.info(f"Build state for build: {build_id} is {state}")

    return jsonify(res), 200

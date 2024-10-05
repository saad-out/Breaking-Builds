from flask import Blueprint, jsonify
from jenkins import JenkinsException
from requests.exceptions import RequestException
import logging

from jenkins_api import (
    server,
    PIPELINE_NAME,
    get_build_stages,
    get_stage_steps,
    get_step_logs
)

# Blueprint for routes
routes_bp = Blueprint('routes_bp', __name__)

# Get logger instance
logger = logging.getLogger(__name__)


@routes_bp.route('/trigger-build', methods=['POST'])
def trigger_build():
    res: dict = {"status": '', "body": {}}

    logger.info("Attempting to trigger build...")

    # Trigger the build
    try:
        queue_item = server.build_job(PIPELINE_NAME)
    except JenkinsException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Error triggering build: {str(e)}"
        logger.error(f"Error triggering build: {str(e)}")
        return jsonify(res), 502
    except RequestException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Network error: {str(e)}"
        logger.error(f"Network error: {str(e)}")
        return jsonify(res), 502
    except TimeoutError as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Request timeout: {str(e)}"
        logger.error(f"Request timeout: {str(e)}")
        return jsonify(res), 504
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        logger.error(f"Unknown error: {str(e)}")
        return jsonify(res), 500

    # Construct response
    res["status"] = "success"
    res["body"]["info"] = {"queue_id": queue_item, "name": PIPELINE_NAME}

    # Log successfull build trigger
    logger.info(f"Build triggered for pipeline: {PIPELINE_NAME}, Build queue id: {queue_item}")

    return jsonify(res), 202

@routes_bp.route('/queue-state/<int:build_id>', methods=['GET'])
def get_build_queue_state(build_id: int):
    res: dict = {"status": '', "body": {}}

    logger.info(f"Getting build queue state for build: {build_id}...")

    # Get the build queue state
    try:
        queue_info = server.get_queue_item(build_id)
    except JenkinsException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Error getting build queue state: {str(e)}"
        logger.error(f"Error getting build queue state: {str(e)}")
        return jsonify(res), 502
    except RequestException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Network error: {str(e)}"
        logger.error(f"Network error: {str(e)}")
        return jsonify(res), 502
    except TimeoutError as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Request timeout: {str(e)}"
        logger.error(f"Request timeout: {str(e)}")
        return jsonify(res), 504
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        logger.error(f"Unknown error: {str(e)}")
        return jsonify(res), 500
    
    # Construct response
    state = ''
    build_number = -1
    if 'executable' in queue_info:
        state = 'left'
        build_number = queue_info['executable']['number']
    elif queue_info.get('cancelled', False) == True:
        state = 'cancelled'
    else:
        state = 'queued'
    res["status"] = "success"
    res["body"]["state"] = state
    if build_number != -1:
        res["body"]["build_number"] = build_number

    # Log build state
    logger.info(f"Build state for build: {build_id} is {state}")

    return jsonify(res), 200

@routes_bp.route('/build-stages/<int:build_number>', methods=['GET'])
def get_stages(build_number: int):
    res: dict = {"status": '', "body": {}}

    logger.info(f"Getting build stages for build: {build_number}...")

    # Get the build stages
    try:
        stages = get_build_stages(build_number)
    except RequestException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Network error: {str(e)}"
        logger.error(f"Network error: {str(e)}")
        return jsonify(res), 502
    except TimeoutError as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Request timeout: {str(e)}"
        logger.error(f"Request timeout: {str(e)}")
        return jsonify(res), 504
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        logger.error(f"Unknown error: {str(e)}")
        return jsonify(res), 500
    
    # Construct response
    stages_info = []
    for stage in stages:
        stages_info.append(
            {
                "id": stage.get('id', ''),
                "name": stage.get('displayName', ''),
                "description": stage.get('displayDescription', ''),
                "state": stage.get('state', ''),
                "status": stage.get('result', ''),
                "start_time": stage.get('startTime', ''),
                "duration": stage.get('durationInMillis', ''),
            }
        )
    res["status"] = "success"
    res["body"]["stages"] = stages_info

    # Log build stages
    logger.info(f"Stages for build: {build_number} gotten successfully")

    return jsonify(res), 200

@routes_bp.route('/build-stages/<int:build_number>/stages/<int:stage_number>/steps', methods=['GET'])
def get_steps(build_number: int, stage_number: int):
    res: dict = {"status": '', "body": {}}

    logger.info(f"Getting stage steps for build: {build_number}, stage: {stage_number}...")

    # Get the stage steps
    try:
        steps = get_stage_steps(build_number, stage_number)
    except RequestException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Network error: {str(e)}"
        logger.error(f"Network error: {str(e)}")
        return jsonify(res), 502
    except TimeoutError as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Request timeout: {str(e)}"
        logger.error(f"Request timeout: {str(e)}")
        return jsonify(res), 504
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        logger.error(f"Unknown error: {str(e)}")
        return jsonify(res), 500

    # Construct response
    steps_info = []
    for step in steps:
        steps_info.append(
            {
                "id": step.get('id', ''),
                "type": step.get('displayName', ''),
                "content": step.get('displayDescription', ''),
                "state": step.get('state', ''),
                "status": step.get('result', ''),
                "start_time": step.get('startTime', ''),
                "duration": step.get('durationInMillis', ''),
            }
        )
    res["status"] = "success"
    res["body"]["steps"] = steps_info

    # Log stage steps
    logger.info(f"Steps for build: {build_number}, stage: {stage_number} gotten successfully")

    return jsonify(res), 200

@routes_bp.route('/build-stages/<int:build_number>/stages/<int:stage_number>/steps/<int:step_number>/logs', methods=['GET'])
def get_logs(build_number: int, stage_number: int, step_number: int):
    res: dict = {"status": '', "body": {}}

    logger.info(f"Getting logs for build: {build_number}, stage: {stage_number}, step: {step_number}...")

    # Get the step logs
    try:
        logs = get_step_logs(build_number, stage_number, step_number)
    except RequestException as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Network error: {str(e)}"
        logger.error(f"Network error: {str(e)}")
        return jsonify(res), 502
    except TimeoutError as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Request timeout: {str(e)}"
        logger.error(f"Request timeout: {str(e)}")
        return jsonify(res), 504
    except Exception as e:
        res["status"] = "failure"
        res["body"]["message"] = f"Unknown error: {str(e)}"
        logger.error(f"Unknown error: {str(e)}")
        return jsonify(res), 500
    
    # Construct response
    res["status"] = "success"
    res["body"]["logs"] = logs

    # Log step logs
    logger.info(f"Logs for build: {build_number}, stage: {stage_number}, step: {step_number} gotten successfully")

    return jsonify(res), 200

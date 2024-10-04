from flask import Blueprint, jsonify
from jenkins import JenkinsException
import logging

from jenkins_api import server, PIPELINE_NAME , get_build_stages

routes_bp = Blueprint('routes_bp', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@routes_bp.route('/trigger-build', methods=['POST'])
def trigger_build():
    res: dict = {"status": '', "body": {}}

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
    res: dict = {"status": '', "body": {}}

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

    # Get the build stages
    stages = get_build_stages(build_number)
    if stages is None:
        res["status"] = "failure"
        res["body"]["message"] = "Error getting build stages"
        return jsonify(res), 500
    
    # Construct response
    stages_info = []
    for stage in stages:
        stages_info.append(
            {
                "type": stage.get('type', ''),
                "name": stage.get('displayName', ''),
                "description": stage.get('displayDescription', ''),
                "state": stage.get('state', ''),
                "status": stage.get('result', ''),
                "start_time": stage.get('startTime', ''),
                "duration": stage.get('durationInMillis', ''),
                "steps_endpoint": stage.get('_links', {}).get('steps', {}).get('href', '')
            }
        )
    res["status"] = "success"
    res["body"]["stages"] = stages_info

    # Log build stages
    logger.info(f"Build stages for build: {build_number} are {stages_info}")

    return jsonify(res), 200

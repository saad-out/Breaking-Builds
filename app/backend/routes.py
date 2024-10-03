from flask import Blueprint, Response, jsonify, make_response
from jenkins import JenkinsException
from time import sleep

from jenkins_api import server, wait_for_build_to_start, PIPELINE_NAME

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/trigger-build', methods=['POST'])
def trigger_build() -> Response:
    res: dict = {"status": None, "info": None}
    try:
        queue_item = server.build_job(PIPELINE_NAME)
        build_number = wait_for_build_to_start(server, queue_item, PIPELINE_NAME)
    except JenkinsException:
        res["status"] = "failure"
        return make_response(jsonify(res), 200)
    build_url = f"{server.server}job/{PIPELINE_NAME}/{build_number}"
    res["status"] = "success"
    res["info"] = {"build_number": build_number, "build_url": build_url, "name": PIPELINE_NAME}
    return make_response(jsonify(res), 200)

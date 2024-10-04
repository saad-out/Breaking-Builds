from jenkins import Jenkins, JenkinsException
import requests
from dotenv import load_dotenv
from os import environ
from time import sleep

load_dotenv()


JENKINS_PORT = environ.get('JENKINS_PORT', '')
JENKINS_URL = environ.get('JENKINS_URL', '')
JENKINS_USERNAME = environ.get('JENKINS_USERNAME', '')
JENKINS_PASSWORD = environ.get('JENKINS_PASSWORD', '')
PIPELINE_NAME = environ.get('PIPELINE_NAME', '')


JENKINS_URL = f"{JENKINS_URL}:{JENKINS_PORT}"
BLUE_OCEAN_URL = f"{JENKINS_URL}/blue/rest/organizations/jenkins"
try:
    server = Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
except JenkinsException:
    raise Exception(f"Error conneting to Jenkins server: {JENKINS_URL}")

def wait_for_build_to_start(server: Jenkins, queue_id: int, name: str) -> int:
    """
    Wait for the build to start
    """
    while True:
        try:
            queue_info = server.get_queue_item(queue_id)
            if 'executable' in queue_info:
                return queue_info['executable']['number']
        except JenkinsException:
            pass
        sleep(1)

def get_build_stages(build_number: int):
    """
    Get the stages of a build
    """
    url = f"{BLUE_OCEAN_URL}/pipelines/{PIPELINE_NAME}/runs/{build_number}/nodes/"
    try:
        res = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return None

def get_stage_steps(build_number: int, stage_number: int):
    """
    Get the steps of a stage
    """
    url = f"{BLUE_OCEAN_URL}/pipelines/{PIPELINE_NAME}/runs/{build_number}/nodes/{stage_number}/steps/"
    try:
        res = requests.get(url, auth=(JENKINS_USERNAME, JENKINS_PASSWORD))
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return None
    

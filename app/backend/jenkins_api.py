from jenkins import Jenkins, JenkinsException
from dotenv import load_dotenv
from os import environ
from time import sleep

load_dotenv()


JENKINS_PORT = environ.get('JENKINS_PORT', '')
JENKINS_URL = environ.get('JENKINS_URL', '')
JENKINS_USERNAME = environ.get('JENKINS_USERNAME', '')
JENKINS_PASSWORD = environ.get('JENKINS_PASSWORD', '')
PIPELINE_NAME = environ.get('PIPELINE_NAME', '')


try:
    URL = f"{JENKINS_URL}:{JENKINS_PORT}"
    server = Jenkins(URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
except JenkinsException:
    raise Exception(f"Error conneting to Jenkins server: {URL}")

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

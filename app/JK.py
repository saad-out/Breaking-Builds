import jenkins
from time import sleep

URL = "http://localhost:8080"
USERNAME = "saadout" 
PASSWORD = "ff2c3aa12ec04ed6bd8d34d853387199"

server = jenkins.Jenkins(url=URL, username=USERNAME, password=PASSWORD)
user = server.get_whoami()
version = server.get_version()
print(f"user {user.get('fullName')} version {version}")

jobs = server.get_all_jobs()
for job in jobs:
    print(f"Job: {job['name']}")

print(server.build_job('fr'))

# server.create_job('test-empty', jenkins.EMPTY_CONFIG_XML)
# sleep(2)
# server.rename_job('test-empty', 'new-test-empty')
# sleep(2)
# server.delete_job('new-test-empty')

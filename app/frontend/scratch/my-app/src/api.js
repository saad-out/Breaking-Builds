import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000';

export const triggerBuild = async () => {
    // try {
    //     const response = await axios.post(`${API_BASE_URL}/trigger-build`);
    //     return response.data;
    // } catch (error) {
    //     console.error('Error triggering build:', error);
    // }
    return {
        "status": "success",
        "body" : {
            "info": {
                "queue_id": 1,
                "name": "my-pipeline",
            }
        }
    };
}

let count = 0;

export const getBuildQueueState = async (buildId) => {
    // try {
    //     const response = await axios.get(`${API_BASE_URL}/queue-state/${buildId}`);
    //     return response.data;
    // } catch (error) {
    //     console.error('Error fetching build queue state:', error);
    // }
    return {
        "status": "success",
        "body" : {
            "state": (count++ < 3) ? 'waiting' : 'left',
            // "state": "cancelled",
            "build_number": 1,
        }
    };
}

let count2 = -1;

export const getBuildStages = async (buildNumber) => {
    // try {
    //     const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}`);
    //     return response.data;
    // } catch (error) {
    //     console.error('Error fetching build stages:', error);
    // }
    count2++;
    return {
        "status": "success",
        "body" : {
            "stages": [
                {
                    "id": 1,
                    "name": "Build",
                    "description": "Build the project",
                    "status": "success",
                    "state": (count2 < 3) ? 'in progress' : 'done',
                },
                {
                    "id": 2,
                    "name": "Test",
                    "description": "Run tests",
                    "status": "success",
                    "state": (count2 < 4) ? 'in progress' : 'done',
                },
                {
                    "id": 3,
                    "name": "Deploy",
                    "description": "Deploy the project",
                    "status": "success",
                    "state": (count2 < 5) ? 'in progress' : 'done',
                },
            ]
        }
    };
}

let count3 = -1;

export const getStageSteps = async (buildNumber, stageId) => {
    // try {
    //     const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps`);
    //     return response.data;
    // } catch (error) {
    //     console.error('Error fetching stage steps:', error);
    // }
    count3++;
    return {
        "status": "success",
        "body" : {
            "steps": [
                {
                    "id": 1,
                    "name": "step 1",
                    "status": "success",
                    "start_time": "2021-09-21T12:00:00",
                    "duration": "1m 30s",
                    "state": (count3 < 3) ? 'in progress' : 'done'
                },
                {
                    "id": 2,
                    "name": "step 2",
                    "status": "success",
                    "start_time": "2021-09-21T12:02:00",
                    "duration": "2m 15s",
                    "state": (count3 < 4) ? 'in progress' : 'done'
                },
                {
                    "id": 3,
                    "name": "step 3",
                    "status": "success",
                    "start_time": "2021-09-21T12:04:00",
                    "duration": "3m 45s",
                    "state": (count3 < 5) ? 'in progress' : 'done'
                },
            ]
        }
    };
}

export const getStepLog = async (buildNumber, stageId, stepId) => {
    // try {
    //     const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps/${stepId}/logs`);
    //     return response.data;
    // } catch (error) {
    //     console.error('Error fetching step log:', error);
    // }
    return {
        "status": "success",
        "body" : {
            "logs": "cd app\nnpm install\nnpm run build\nnpm run test"
        }
    };
}

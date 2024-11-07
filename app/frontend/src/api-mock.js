import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000';

export const triggerBuild = async () => {
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
                    "state": (count2 < 3) ? 'in progress' : 'FINISHED',
                },
                {
                    "id": 2,
                    "name": "Test",
                    "description": "Run tests",
                    "status": "success",
                    "state": (count2 < 4) ? 'in progress' : 'FINISHED',
                },
                {
                    "id": 3,
                    "name": "Deploy",
                    "description": "Deploy the project",
                    "status": "success",
                    "state": (count2 < 5) ? 'in progress' : 'FINISHED',
                },
            ]
        }
    };
}

let count3 = -1;

export const getStageSteps = async (buildNumber, stageId) => {
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
                    "state": (count3 < 3) ? 'in progress' : 'FINISHED'
                },
                {
                    "id": 2,
                    "name": "step 2",
                    "status": "success",
                    "start_time": "2021-09-21T12:02:00",
                    "duration": "2m 15s",
                    "state": (count3 < 4) ? 'in progress' : 'FINISHED'
                },
                {
                    "id": 3,
                    "name": "step 3",
                    "status": "success",
                    "start_time": "2021-09-21T12:04:00",
                    "duration": "3m 45s",
                    "state": (count3 < 5) ? 'in progress' : 'FINISHED'
                },
            ]
        }
    };
}

export const getStepLog = async (buildNumber, stageId, stepId) => {
    return {
        "status": "success",
        "body" : {
            "logs": "cd app\nnpm install\nnpm run build\nnpm run test"
        }
    };
}

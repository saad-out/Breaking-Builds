import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const triggerBuild = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/trigger-build`);
        return response.data;
    } catch (error) {
        console.error('Error triggering build:', error);
    }
}

export const getBuildQueueState = async (buildId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/queue-state/${buildId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching build queue state:', error);
    }
}

export const getBuildStages = async (buildNumber) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching build stages:', error);
    }
}

export const getStageSteps = async (buildNumber, stageId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps`);
        return response.data;
    } catch (error) {
        console.error('Error fetching stage steps:', error);
    }
}

export const getStepLog = async (buildNumber, stageId, stepId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps/${stepId}/logs`);
        return response.data;
    } catch (error) {
        console.error('Error fetching step log:', error);
    }
}

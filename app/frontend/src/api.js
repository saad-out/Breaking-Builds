import axios from 'axios';

const API_BASE_URL = "https://breaking-builds.onrender.com";

export const pingServer = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/ping`);
        return response.data;
    } catch (error) {
        console.error('Error pinging server:', error);
        return null;
    }
}

export const triggerBuild = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/trigger-build`);
        return response.data;
    } catch (error) {
        console.error('Error triggering build:', error);
        return null;
    }
}

export const getBuildQueueState = async (buildId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/queue-state/${buildId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching build queue state:', error);
        return null;
    }
}

export const getBuildStages = async (buildNumber) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching build stages:', error);
        return null;
    }
}

export const getStageSteps = async (buildNumber, stageId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps`);
        return response.data;
    } catch (error) {
        console.error('Error fetching stage steps:', error);
        return null;
    }
}

export const getStepLog = async (buildNumber, stageId, stepId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/build-stages/${buildNumber}/stages/${stageId}/steps/${stepId}/logs`);
        return response.data;
    } catch (error) {
        console.error('Error fetching step log:', error);
        return null;
    }
}

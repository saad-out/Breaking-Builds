import React, { useState, useEffect } from 'react';
import './App.css';
import StageCards from './StageCards';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
    triggerBuild,
    getBuildQueueState,
    getBuildStages,
} from './api';
import Spinner from 'react-bootstrap/Spinner';


function App() {
    const [showStages, setShowStages] = useState(false);
    const [stages, setStages] = useState([]); // TODO: load with initial empty data
    const [buildNumber, setBuildNumber] = useState(-1);
    const [triggerButtonState, setTriggerButtonState] = useState('Trigger');
    
    const handleButtonClick = async () => {
        if (triggerButtonState === 'Trigger') {

            setTriggerButtonState('Triggering...');
            const data = await triggerBuild();
            const queue_id = data['body']['info']['queue_id'];

            const interval = setInterval(async () => {
                console.log('Checking build queue state');
                const data = await getBuildQueueState(queue_id);
                if (data['body']['state'] === 'left')
                {
                    setBuildNumber(data['body']['build_number']);
                    setTriggerButtonState('Triggered ✅');
                    clearInterval(interval);
                }
                else if (data['body']['state'] === 'cancelled')
                {
                    setTriggerButtonState('Error ❌');
                    clearInterval(interval);
                }
            }, 1000);
        }
    };

    useEffect(() => {
        if (buildNumber !== -1) {
            const interval = setInterval(async () => {
                console.log('Fetching build stages');
                const data = await getBuildStages(buildNumber);
                setStages(data['body']['stages']);
                setShowStages(true);
                let allDone = true;
                for (let stage of data['body']['stages']) {
                    if (stage['state'] !== 'FINISHED') {
                        allDone = false;
                        break;
                    }
                }
                if (allDone) {
                    clearInterval(interval);
                }
            }, 1000);

            // Avoid memory leak
            return () => clearInterval(interval);
        }
    }, [buildNumber]);

    return (
        <div className="container">
        <h1 className="title">Breaking Builds</h1>
        <p className="description">Realtime Full CI/CD Pipeline with Jenkins</p>
        <button className={ (triggerButtonState !== 'Trigger') ? "button-disabled" : "trigger-button" } onClick={handleButtonClick} disabled={ (triggerButtonState !== 'Trigger') }>
            { (triggerButtonState === 'Trigger') ? 'Trigger Build 👨‍🍳' : triggerButtonState }
            {/* <Spinner animation="border" role="status"> */}
            {/*     <span className="visually-hidden">Loading...</span> */}
            {/* </Spinner> */}
        </button>
        {showStages && <StageCards buildNumber={buildNumber} stages={stages} />}
        </div>
    );
}

export default App;


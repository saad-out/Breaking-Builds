// StageCards.js
import React, { useState } from 'react';
import './App.css';
import CustomModal from './Modal';
import { getStageSteps } from './api';

const StageCards = ({ buildNumber, stages }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [steps, setSteps] = useState({});
  const [currentSteps, setCurrentSteps] = useState([]); // TODO: load with initial empty data

  const openModal = (stage) => {
      if (stage['state'] === 'FINISHED' && !(stage['id'] in steps)) {
          const interval = setInterval(async () => {
              const data = await getStageSteps(buildNumber, stage['id']);
              let _steps = data['body']['steps'];
              _steps["stageId"] = stage['id'];
              _steps["done"] = true;
              setCurrentSteps(_steps);
              let allDone = true;
              for (let step of _steps) {
                  if (step['state'] !== 'FINISHED') {
                      allDone = false;
                      break;
                  }
              }

              if (allDone) {
                // Make a copy of steps and set it with new data
                setSteps((prevSteps) => {
                    const updatedSteps = { ...prevSteps, [stage['id']]: _steps };
                    // Update current steps to trigger re-render for this specific modal
                    setCurrentSteps(_steps);
                    return updatedSteps;
                });
                clearInterval(interval);
              } else {
                setCurrentSteps(_steps);
              }

              // if (allDone) {
              //     steps[stage['id']] = _steps;
              //     setSteps(steps);
              //     clearInterval(interval);
              // }
          }, 3000);
      } else if (stage['state'] !== 'FINISHED') {
          setCurrentSteps({"done": false});
      } else {
          setCurrentSteps(steps[stage['id']]);
      }
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <div className="stage-cards-container">
      {
           stages.map((stage, index) => {
            const stageTitle = stage['name'];
            const stageState = stage['state'];
            const _stage = {
                "id": stage['id'],
                "title": stageTitle,
                "state": stageState,
                "steps": [],
            };

            return (
            <div key={index}
                className={`stage-card ${stageState ? `stage-${stageState.toLowerCase()}` : 'stage-waiting'}`}
                onClick={() => openModal(_stage)} disabled={stageState !== 'FINISHED'}>
                <h2 className="stage-title">{stageTitle}</h2>
                <h5>{stageState !== null ? stageState : 'waiting'}</h5>
            </div>
            );
        })
      }
      <CustomModal
        buildNumber={buildNumber}
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        steps={currentSteps}
      />
    </div>
  );
};

export default StageCards;


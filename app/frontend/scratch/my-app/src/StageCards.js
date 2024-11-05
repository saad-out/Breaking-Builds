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
      if (stage['state'] === 'done' && !(stage['id'] in steps)) {
          const interval = setInterval(async () => {
              console.log('Fetching stage steps for stage:', stage['id']);
              const data = await getStageSteps(buildNumber, stage['id']);
              let _steps = data['body']['steps'];
              _steps["stageId"] = stage['id'];
              _steps["done"] = true;
              setCurrentSteps(_steps);
              console.log('steps:', _steps);
              let allDone = true;
              for (let step of _steps) {
                  if (step['state'] !== 'done') {
                      allDone = false;
                      break;
                  }
              }
              if (allDone) {
                  steps[stage['id']] = _steps;
                  setSteps(steps);
                  clearInterval(interval);
              }
          }, 1000);
      } else if (stage['state'] !== 'done') {
          setCurrentSteps({"done": false});
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
            <div key={index} className="stage-card" onClick={() => openModal(_stage)}>
                <h2 className="stage-title">{stageTitle}</h2>
                <h5>{stageState}</h5>
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


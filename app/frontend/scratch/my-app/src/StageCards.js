// // StageCards.js
// import React, { useState } from 'react';
// import './App.css';
// import CustomModal from './Modal';
//
// const StageCards = ({ stages }) => {
//   const [modalIsOpen, setModalIsOpen] = useState(false);
//   const [currentSteps, setCurrentSteps] = useState([]);
//
//   const openModal = (steps) => {
//     setCurrentSteps(steps);
//     setModalIsOpen(true);
//   };
//
//   const closeModal = () => {
//     setModalIsOpen(false);
//   };
//
//   return (
//     <div className="stage-cards-container">
//       {stages.map((stage, index) => {
//         const stageTitle = Object.keys(stage)[0];
//         const steps = stage[stageTitle];
//
//         return (
//           <div key={index} className="stage-card" onClick={() => openModal(steps)}>
//             <h2 className="stage-title">{stageTitle}</h2>
//           </div>
//         );
//       })}
//       <CustomModal
//         isOpen={modalIsOpen}
//         onRequestClose={closeModal}
//         steps={currentSteps}
//       />
//     </div>
//   );
// };
//
// export default StageCards;
//
// StageCards.js
import React, { useState } from 'react';
import './App.css';
import CustomModal from './Modal';

const StageCards = ({ stages }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [currentSteps, setCurrentSteps] = useState([]);

  const openModal = (steps) => {
    setCurrentSteps(steps);
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <div className="stage-cards-container">
      {stages.map((stage, index) => {
        const stageTitle = Object.keys(stage)[0];
        const steps = stage[stageTitle];

        return (
          <div key={index} className="stage-card" onClick={() => openModal(steps)}>
            <h2 className="stage-title">{stageTitle}</h2>
          </div>
        );
      })}
      <CustomModal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        steps={currentSteps}
      />
    </div>
  );
};

export default StageCards;


// Modal.js
import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import './App.css';

const color = '#5c590b';

const CustomModal = ({ isOpen, onRequestClose, steps }) => {
  return (
    <Modal show={isOpen} onHide={onRequestClose} centered>
      <Modal.Header closeButton style={{ backgroundColor: color }}>
        <Modal.Title>Steps</Modal.Title>
      </Modal.Header>
      <Modal.Body style={{ backgroundColor: color }}>
        {steps.map((step, index) => {
          const stepTitle = Object.keys(step)[0];
          const stepData = step[stepTitle];

          return (
            <div key={index} className="step">
              <h5>{stepTitle}</h5>
              <p>{stepData.log}</p>
              <a href={stepData.link} target="_blank" rel="noopener noreferrer">
                View Logs
              </a>
            </div>
          );
        })}
      </Modal.Body>
      <Modal.Footer style={{ backgroundColor: color }}>
        <Button variant="secondary" onClick={onRequestClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CustomModal;

// Modal.js
import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import './App.css';
import { getStepLog } from './api';

const color = '#5c590b';

const CustomModal = ({ buildNumber, isOpen, onRequestClose, steps }) => {

    const handleViewLogsClick = async (stepId) => {
    try {
      // Fetch the logs using the provided async function
      const logs = await getStepLog(buildNumber, steps['stageId'], stepId);
      
      // Open a new window/tab and display the logs
      const newWindow = window.open('', '_blank');
      newWindow.document.write(`
        <html>
          <head>
            <title>Logs</title>
            <style>
              body {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Courier New', Courier, monospace;
                padding: 20px;
              }
              pre {
                white-space: pre-wrap; /* Wrap the text if it’s too long */
                overflow-x: auto;
              }
            </style>
          </head>
          <body>
            <h3>Logs</h3>
            <pre>${logs['body']['logs']}</pre>
          </body>
        </html>
      `);
      newWindow.document.close();
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };


  return (
    <Modal show={isOpen} onHide={onRequestClose} centered>
      <Modal.Header closeButton style={{ backgroundColor: color }}>
        <Modal.Title>Steps</Modal.Title>
      </Modal.Header>
      { steps["done"] === false ?
        <Modal.Body style={{ backgroundColor: color }}>
          <h5>Loading...</h5>
        </Modal.Body>
        :
        <Modal.Body style={{ backgroundColor: color }}>
          {steps.map((step, index) => {
            return (
              <div key={index} className="step">
                <h5>{step["name"]}</h5>
                <p>{"state: " + step['state']}</p>
                <p>{"start_time: " + step['start_time']}</p>
                <p>{"duration: " + step['duration']}</p>

                {/* "View Logs" link that opens logs in a new tab */}
                <button
                    className="view-logs-button"
                    onClick={() => handleViewLogsClick(step["id"])}
                >
                    View Logs
                </button>

                {/* Bash-style code block for logs */}
                {/* <pre className="bash-code-block"> */}
                {/*     {/* <code>{step['log']}</code> */}
                {/*     <code>{"cd app"}</code> */}
                {/* </pre> */}

                {/* <p>{stepData.log}</p> */}
                {/* <a href={stepData.link} target="_blank" rel="noopener noreferrer"> */}
                {/* <a href={`localhost:3000/build-stages/${buildNumber}/stages/${steps['stageId']}/steps/${step['id']}/logs`} target="_blank" rel="noopener noreferrer"> */}
                {/*   View Logs */}
                {/* </a> */}
              </div>
            );
          })}
        </Modal.Body>
      }
      <Modal.Footer style={{ backgroundColor: color }}>
        <Button variant="secondary" onClick={onRequestClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CustomModal;


import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="container">
        <h1 className="title">
            Breaking Builds
        </h1>
        <p className="description">
            Realtime Full CI/CD Pipeline with Jenkins.
        </p>
        <button className="trigger-button">
            Trigger Build
        </button>
    </div>
  );
}

export default App;

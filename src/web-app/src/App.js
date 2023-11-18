import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import './ImageUpload'
import InputBox from './inputBox';
import DataSetBox from './dataSetBox';
import Search from './search';
import AboutUs from './AboutUs';
import CameraOn from './cameraOn';

function App() {
  return (
    <Router>
      <div className="App-header">
        <div className="HeadTab">
          <Link to="/" id="ButtonHead1" className="navbar-button">Home</Link>
          <Link to="/camera-on" className="navbar-button">Camera</Link>
          <Link to="/about-us" id="ButtonHead3" className="navbar-button">About Us</Link>
        </div>
        <Routes>
          <Route path="/camera-on" element={<CameraOn/>}/>
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/" element={
            <>
              <h2 style={{position:'relative',right:'35vw',top:'40vh',color:'white',fontSize:'4vh'}}>
              Input The Image</h2>
              <div  className="boxInputImage">
                <InputBox>
                </InputBox>
              </div>
              <h2 style={{position:'relative',left:'0vw',top:'70vh',color:'white',fontSize:'4vh'}}> Input The Data Set</h2>
                <DataSetBox/>
              <div className="resultBox">
                  <Search/>
              </div>
            </>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

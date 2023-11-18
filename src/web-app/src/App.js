import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import './ImageUpload'
import ImageUpload from './ImageUpload';
import MultiImageUpload from "./multiImageUpload";
import Search from './search';
import AboutUs from './AboutUs';
import HowToUse from './howToUse';
import Cbir from './cbir';

function App() {
  return (
    <Router>
      <div className="App-header">
        <div className="HeadTab">
          
          <Link to="/" id="ButtonHead1" className="navbar-button">Home</Link>
          <Link to="/howtouse" id="ButtonHead3" className="navbar-button">How To Use</Link>
          <Link to="/about-us" id="ButtonHead3" className="navbar-button">About Us</Link>
        </div>
        <Routes>
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/howtouse" element={<HowToUse />} />
          <Route path="/cbir" element={<Cbir/>}/>
          <Route path="/" element={
            <>
              <h1 style={{position:'relative', top:'20vh'}}> Image Search Engine</h1>
              <div className='doYouKnow' style={{position:'relative', top:'40vh', left:'27vw', fontSize:'3vh'}}>
                <h2> Fun Fact !</h2>
                <p> Search engine pada program ini menggunakan<br></br>
                algoritma CBIR atau Content-Based Information Retrieval (CBIR).<br></br> Jika ingin mencari tahu lebih lanjut, <br></br>
                  silahkan tekan link di bawah ini</p>
                  <Link to="/cbir" className='link'> (more Information) </Link>
              </div>
              <h2 style={{position:'relative',right:'35vw',top:'40vh',color:'white',fontSize:'4vh'}}>
              Input The Image</h2>
              <div  className="boxInputImage">
                <ImageUpload/>
              </div>
              <h2 style={{position:'relative',left:'0vw',top:'70vh',color:'white',fontSize:'4vh'}}> Input The Data Set</h2>
                <MultiImageUpload/>
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

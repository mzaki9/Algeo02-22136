import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import './ImageUpload'
import InputBox from './inputBox';
import DataSetBox from './dataSetBox';
import Search from './search';
import CameraComponent from './camera';
function CameraOn() {
    return(
        <>
         <div style={{position:'relative', bottom:'0vh'}}>
                <CameraComponent/>
            </div>
            <h2 style={{position:'relative',right:'35vw',top:'40vh',color:'white',fontSize:'4vh'}}>
            Input The Images</h2>
            
            <div  className="boxInputImage">

            </div>
            
            <h2 style={{position:'relative',left:'0vw',top:'70vh',color:'white',fontSize:'4vh'}}> Input The Data Set</h2>
            <DataSetBox/>
            <div className="resultBox">
                <Search/>
            </div>
        </>
    );
}
export default CameraOn;
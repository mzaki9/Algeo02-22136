import React from 'react';
import './App.css';
import './ImageUpload'
import ImageUpload from './ImageUpload';
import MultiImageUpload from "./multiImageUpload";
import Search from './search';
import CameraComponent from './camera';

function CameraOn() {
    return(
        <>
             <div style={{position:'relative', bottom:'0vh'}}>
                 <CameraComponent/>
            </div>
              
              <h2 style={{position:'relative',left:'0vw',top:'70vh',color:'white',fontSize:'4vh'}}> Input The Data Set</h2>
                <MultiImageUpload/>
              <div className="resultBox">
                  <Search/>
              </div>
        </>
    );
}
export default CameraOn;
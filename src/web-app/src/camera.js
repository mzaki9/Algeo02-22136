import React, { useRef, useState, useEffect } from 'react';
import './camera.css'

const Camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [timer, setTimer] = useState(5);
  const [stream, setStream] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [intervalId, setIntervalId] = useState(null);
  const [showCamera, setShowCamera] = useState(true);
  const [file,setFile] = useState(null);
  const [switchState, setSwitchState] = useState(false);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.play();
        setCameraActive(true);
      }
      const id = setInterval(() => {
        setTimer((prevTimer) => (prevTimer > 1 ? prevTimer - 1 : 5)); // Reset to 5 if it's 0
      }, 1000);
      setIntervalId(id);
    } catch (error) {
      console.error('Error accessing the camera:', error);
    }
  };

  const stopCamera = () => {
    if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
      if (intervalId) {
        clearInterval(intervalId); // Clear the timer interval
        setIntervalId(null); // Clear interval ID
      }
      setTimer(5);
      setCameraActive(false);
      setStream(null);
      console.log('Camera stopped. Timer reset.');
  };

  const captureImage = async() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video && canvas) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imgData = canvas.toDataURL('image/png');
      const blob = dataURItoBlob(imgData);
      const url = URL.createObjectURL(blob);
      setFile(url);
      try{
        const formData = new FormData();
        formData.append('file', blob, 'image.png');
        const response = await fetch('http://localhost:5000/upload' ,{
          method:'POST',
          body: formData,
        });
        const data = await response.json();
        console.log(data);

      }catch (error){
        console.error('Error uploading file:', error);
      }

    }
  };

  useEffect(() => {
    if (stream && cameraActive) {
      const id = setInterval(() => {
        captureImage();
      }, 5000);
      setIntervalId(id);

      return () => {
        stopCamera(); 
      };
    }
  }, [stream, cameraActive]);
  const handleSwitchToggle = () => {
    setSwitchState(!switchState);
    if (!switchState) {
        startCamera();
    } else {
        stopCamera();
    }
  };

  return (
    <>
    <h2 style={{position:'relative',top:'345px',left:'145px'}}> camera</h2>
    <div className='camera-container'>
      {showCamera && (
        <video
          ref={videoRef}
          style={{ maxWidth: '320px', maxHeight: '240px', position:'relative',top:'15px'}}
        />
      )}
      </div>
      <div style={{position:'relative',left:'440px', top:'100px'}}>
          <h4 style={{position:'relative',top:'15px',left:'15px',fontSize:'4vh'}}> TURN</h4>
          <p style={{position:'relative', bottom:'0px',left:'60px'}}>on</p>
          <p style={{position:'relative', bottom:'49px',right:'0px'}}>off</p>
      
      <label class="switch-cam" style={{position:'relative', bottom:'50px'}}>
          <input type="checkbox" id="mySwitch" checked={switchState} onChange={handleSwitchToggle}/>
          <span class="slider-cam"></span>
        </label>
      </div>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <div className='timer'>Timer: {timer}</div>
      <h2 style={{position:'relative',right:'35vw',top:'220px',right:'265px',color:'white',fontSize:'4vh'}}>
              The Input Image</h2>
      <div className='boxSnapImage'>
          
      <img src={file}  style={{position:'relative',
              minHeight:'240px',minWidth:'240px', maxHeight:'350px',maxWidth:'350px',top:'20px'}}/>
      </div>
    </>
    
  );
};

function dataURItoBlob(dataURI) {
  const byteString = atob(dataURI.split(',')[1]);
  const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: mimeString });
}

export default Camera;

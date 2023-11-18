import React, { useRef, useState, useEffect } from 'react';

const Camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [timer, setTimer] = useState(5);
  const [stream, setStream] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [intervalId, setIntervalId] = useState(null);
  const [flash, setFlash] = useState(false);
  const [showCamera, setShowCamera] = useState(true);

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

  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video && canvas) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imgData = canvas.toDataURL('image/png');
      console.log(imgData);
    }
  };

  useEffect(() => {
    if (stream && cameraActive) {
        if (timer === 2) {
            const flashTimeout = setTimeout(() => {
              setShowCamera(false); 
              setFlash(true);
              setTimeout(() => {
                setShowCamera(true); 
                setTimer(5); 
                setFlash(false);
              }, 1000);
            }, 0);
            return () => clearTimeout(flashTimeout);
        }
      const id = setInterval(() => {
        captureImage();
      }, 5000);
      setIntervalId(id);

      return () => {
        stopCamera(); 
      };
    }
  }, [stream, cameraActive]);

  useEffect(() => {
    if (!stream && intervalId) {
      clearInterval(intervalId);
      setTimer(5);
      setCameraActive(false);
      console.log('Camera stopped. Timer reset.');
    }
  }, [stream, intervalId]);

  return (
    <>
      {flash ? (
        <div
          style={{
            width: '100%',
            height: '100%',
            backgroundColor: 'black',
            position: 'relative',
            zIndex: 999,
            opacity: 0.5,
          }}
        ></div>
      ) : null}
      {showCamera && (
        <video
          ref={videoRef}
          style={{ maxWidth: '640px', maxHeight: '480px' }}
        />
      )}
      <button onClick={startCamera}>Start Camera</button>
      <button onClick={stopCamera}>Stop Camera</button>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <div>Timer: {timer}</div>
    </>
    
  );
};

export default Camera;

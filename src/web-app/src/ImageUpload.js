import React, { useRef, useState } from 'react';
function ImageUpload(){
    const [file, setFile] = useState(null);
    const handleFile = async (e)=>{
      const selectedFile = e.target.files[0];
      console.log(e.target.files);
      setFile(URL.createObjectURL(e.target.files[0]));
      try{

        const formData = new FormData();
        formData.append('file', selectedFile);
        const response = await fetch('http://127.0.0.1:5000/upload' ,{
          method:'POST',
          body: formData,
        });
        const data = await response.json();
        console.log(data);
      } catch (error){
        console.error('Error uploading file:', error);
      }
    }
    const hiddenFile = useRef(null);

    const handleClick = event =>{
      hiddenFile.current.click();
    };
    return (
      <div>
          <div onClick={handleClick} style={{cursor:'pointer'}}>
            Upload a file
          </div>
          <input
            type="file"
            ref = {hiddenFile}
            style={{display:'none'}}
            onChange={handleFile}
          />
            {file && (
            <img src={file} alt="Uploaded" style={{position:'relative',
            minHeight:'240px',minWidth:'240px', maxHeight:'400px',maxWidth:'400px',bottom:'390px'}}/>


          )}
        </div>
    );
}

  export default ImageUpload;
import React, { useRef, useState } from 'react';
import './App.css'
import './pagination.css'

function ImageUpload(){
    const [file, setFile] = useState(null);
    const handleFile = async (e)=>{
      const selectedFile = e.target.files[0];
      console.log(e.target.files);
      setFile(URL.createObjectURL(e.target.files[0]));
      try{

        const formData = new FormData();
        formData.append('file', selectedFile);
        const response = await fetch('http://localhost:5000/upload' ,{
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
         <div style={{position:'relative', top:'90px', left:'320px'}}>
            <label class="custom-file-upload">
                <input type="file" style={{display:'none', cursor:'pointer'}} onChange={handleFile} />
                Upload File
            </label>
          </div>

          <div className="uploadImageButton">
            <div onClick={handleClick} style={{cursor:'pointer', opacity:'0.25'}}>
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
              minHeight:'240px',minWidth:'240px', maxHeight:'350px',maxWidth:'350px',bottom:'350px'}}/>


            )}
          </div>
        </div>
    );
}

  export default ImageUpload;
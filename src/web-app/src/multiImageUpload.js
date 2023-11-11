import React, { useRef, useState } from 'react';

function MultiImageUpload(){
    const [files, setFile] = useState([]);
    const hiddenFile = useRef(null);

    const handleFile = async (e)=>{
      const selectedFiles = e.target.files;
      console.log(e.target.files);
      const firstTwoImages = [];
      if (selectedFiles.length>2){
        for (let i=0;i<2;i++){
            const url = URL.createObjectURL(selectedFiles[i]);
            firstTwoImages.push(url);
        }

      }else{
        for (let i=0;i<selectedFiles.length;i++){
            const url = URL.createObjectURL(selectedFiles[i]);
            firstTwoImages.push(url);
        }
      }
      setFile(firstTwoImages);
      try{
        const formData = new FormData();
        for (let i=0;i<selectedFiles.length;i++){
            formData.append('files', selectedFiles[i]);
        }
        const response = await fetch('http://127.0.0.1:5000/multiupload' ,{
          method:'POST',
          body: formData,
        });
        const data = await response.json();
        console.log(data);
      } catch (error){
        console.error('Error uploading file:', error);
      }
    }
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
            multiple
          />
            {files.map((url, index) => (
                <img
                key={index}
                src={url}
                alt={`Uploaded ${index + 1}`}
                style={{
                    position: 'relative',
                    minHeight: '200px',
                    minWidth: '200px',
                    maxHeight: '300px',
                    maxWidth: '300px',
                    bottom: '390px',
                    marginRight: '30px', // Add some space between images
                }}
                />
            ))}
        </div>
    );
}
export default MultiImageUpload;
import React, { useState } from 'react';
function ImageUpload() {
    const [selectedImage, setSelectedImage] = useState(null);
  
    const handleImageChange = (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload= (e)=>{
            const imgURL = e.target.result;
            const img = new Image();
            img.src = imgURL;
    
            const maxWidth = 270;
            const maxHeight = 338;
            let newWidth = img.width;
            let newHeight = img.height;

            if (img.width > maxWidth) {
                newWidth = maxWidth;
                newHeight = (img.height * maxWidth) / img.width;
              }
      
            if (newHeight > maxHeight) {
                newHeight = maxHeight;
                newWidth = (img.width * maxHeight) / img.height;
            }
            const canvas = document.createElement('canvas');
            canvas.width = newWidth;
            canvas.height = newHeight;
    
            // Draw the resized image on the canvas
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, newWidth, newHeight);
    
            // Convert the canvas to a data URL
            const resizedDataUrl = canvas.toDataURL('image/jpeg');
            setSelectedImage(resizedDataUrl);             
        };
        reader.readAsDataURL(file);
      }
    };
/*
    const handleImageUpload = () => {
        // form data -> post request server
        const formData = new FormData();
        formData.append('image', image);

       // fecth (send image) using flask->axios request
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    };
    */
    return (
      <div>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          id="imageInput"
          style={{ display: 'none'}}
        />
        <button onClick={() => document.getElementById('imageInput').click()}>
          Upload Image
        </button>
        {selectedImage && <img src={selectedImage} alt="Selected" style={{position:'absolute', bottom:'25px', left:'-5px'}}/>}
      </div>
    );
  }
  
  export default ImageUpload;
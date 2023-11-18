import React, { useRef, useState } from 'react';
import ReactPaginate from 'react-paginate';
import './App.css'
import './pagination.css'
function MultiImageUpload(){
    const [files, setFile] = useState([]);
    const hiddenFile = useRef(null);

    const handleFile = async (e)=>{
      const selectedFiles = e.target.files;
      console.log(e.target.files);
      const images= [];

        for (let i=0;i<selectedFiles.length;i++){
            const url = URL.createObjectURL(selectedFiles[i]);
            images.push(url);
        }
      setFile(images);
      console.log(images);
      try{
        const formData = new FormData();
        for (let i=0;i<selectedFiles.length;i++){
            formData.append('files', selectedFiles[i]);
        }
        const response = await fetch('http://localhost:5000/multiupload' ,{
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
        <div style={{position:'relative', top:'650px', right:'170px'}}>
        <label class="custom-file-upload">
            <input type="file" style={{display:'none'}} onChange={handleFile} multiple/>
          Upload File
        </label>
        </div>
        <div  className="dataBox">
          <div className='uploadDataSetButton'>
            <div onClick={handleClick} style={{cursor:'pointer',opacity:'0.25',left:'0vw',position:'relative'}}>
              <h4>
                  Upload Images
              </h4>
            </div>
            <input
              type="file"
              ref = {hiddenFile}
              style={{display:'none'}}
              onChange={handleFile}
              multiple
            />
            <PaginatedItems itemsPerPage={2} items={files}/>
            </div>
          </div>
        </div>
    );
}


function Items({ currentItems}) {
    return (
      <>
        {currentItems &&
           currentItems.map((url, index) => (
            <img
            key={index}
            src={url}
            style={{
                position: 'relative',
                bottom: '350px',
                minHeight: '200px',
                minWidth: '200px',
                maxHeight: '280px',
                maxWidth: '280px',
                marginRight: '40px', // Add some space between images
            }}
            />
        ))}
      </>
    );
  }

function PaginatedItems({ itemsPerPage, items}) {
  
    const [itemOffset, setItemOffset] = useState(0);
  
 
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    const currentItems = items.slice(itemOffset, endOffset);
    const pageCount = Math.ceil(items.length / itemsPerPage);
  
    
    const handlePageClick = (event) => {
      const newOffset = (event.selected * itemsPerPage) % items.length;
      console.log(
        `User requested page number ${event.selected}, which is offset ${newOffset}`
      );
      setItemOffset(newOffset);
    };
  
    return (
      <>
        <Items currentItems={currentItems} />
        <div style={{position:'absolute',top:'230px',left:'0vw'}}>
            <ReactPaginate
                    breakLabel="..."
                    nextLabel="next >"
                    onPageChange={handlePageClick}
                    pageRangeDisplayed={2}
                    marginPagesDisplayed={2}
                    pageCount={pageCount}
                    previousLabel="< prev"

                    containerClassName={'react-paginate'}
                    activeClassName={'active'}
                    pageClassName={'page-item'}
                    previousClassName={'page-item'}
                    nextClassName={'page-item'}
                    breakClassName={'page-item'}
                    pageLinkClassName={'page-link'}
                    previousLinkClassName={'page-link'}
                    nextLinkClassName={'page-link'}
                    breakLinkClassName={'page-link'}
                    renderOnZeroPageCount={null}
                  />
        </div>
      </>
    );
  }
export default MultiImageUpload;
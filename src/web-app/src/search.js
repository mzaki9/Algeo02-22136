import React, { useRef, useState } from 'react';
import ReactPaginate from 'react-paginate';
import './search.css'
import './pagination';

function Search(){
    const [SwitchVal, setSwitchVal] = useState(1); 
    const [timeExec, setTimeExec] = useState(0);
    const [tupleList, setTupleList] = useState([]);
    const [files, setFiles] = useState([]);
    const [switchState, setSwitchState] = useState(false);


    const searchImg = async ()=>{
        if (SwitchVal===1){
            console.log("CBIR texture");
            try{
                const response = await fetch('http://localhost:5000/cbirtexture',{
                    method:'GET',
                });
                const jsonData = await response.json();
                setTimeExec(jsonData.execution_time);
                setTupleList(jsonData.results || []);
                console.log(jsonData);
                const img = [];
                  for (let i=0;i<jsonData.results.length;i++){
                    img.push(jsonData.results[i][0]);
                  }
                const imageContext = require.context('../DataSet', false, /\.(png|jpe?g|svg)$/);
                const images = importAll(imageContext);
                setFiles(images)
    
            }catch(error){
                console.log('Error request to API',error)
            }
        }else{
            console.log("CBIR warna");
            try{
                const response = await fetch('http://localhost:5000/cbirwarna',{
                    method:'GET',
                });
                const jsonData = await response.json();
                setTimeExec(jsonData.execution_time);
                setTupleList(jsonData.results || []);
                console.log(jsonData);
                const img = [];
                  for (let i=0;i<jsonData.results.length;i++){
                    img.push(jsonData.results[i][0]);
                  }
                const imageContext = require.context('../DataSet', false, /\.(png|jpe?g|svg)$/);
                const images = importAll(imageContext);
                setFiles(images)
      
            }catch(error){
                console.log('Error request to API',error)
            }
        }
    };
    const handleSwitchClick = ()=>{ // switch CBIR mode
        setSwitchVal(SwitchVal*-1);
        console.log(SwitchVal);
    };
    
    const handleSwitchToggle = () => {
      setSwitchState(!switchState); // Toggle the switch state
      // Perform actions based on the switch state
      if (!switchState) {
        setSwitchVal(-1);
      } else {
        setSwitchVal(1);
      }
      console.log(SwitchVal);
    };
    return(
        <div>
            <div style={{position:'relative', bottom:'190px', right:'38vw'}}>
                <h3>
                    Switch CBIR mode:
                </h3>
                <h4 style={{position:'relative',bottom:'25px'}}>
                  <div style={{right:'60px',position:'relative', fontSize:'4vh'}}>
                    tekstur
                  </div>
                  <div style={{left:'60px',position:'relative', bottom:'30px',fontSize:'4vh'}}>
                    warna
                  </div>
                </h4>
                <label class="switch" style={{position:'relative', bottom:'50px'}}>
                  <input type="checkbox" id="mySwitch" checked={switchState} onChange={handleSwitchToggle}/>
                  <span class="slider"></span>
                </label>
            </div>

            <button  onClick={searchImg} className="Searchbtn"style={{position:'relative',bottom:'330px', fontSize:'6vh'}}>
                SEARCH
            </button>
            <h3 style={{position:'relative',bottom:'400px',color:'white',fontSize:'4vh', left:'420px'}}>
              Result: {tupleList.length} gambar
            </h3>
            <h3 style={{position:'relative',bottom:'410px',color:'white',fontSize:'4vh', left:'400px'}}>
              time: {timeExec.toFixed(3)} s
            </h3>
            
            {tupleList.length >0 && ( // Conditionally render only if tupleList has data
                <PaginatedItems itemsPerPage={3} items={tupleList} data={files} />
              )}
        </div>
    );
}
function importAll(r) {
  let images = {};
  r.keys().forEach((fileName) => {
    images[fileName.slice(2,fileName.length)] = r(fileName);
  });
  return images;
}

function Items({ currentItems, data}) {
  const imageElmt = currentItems.map((item, index) => (
    <div key={index} style={{ position:'relative', flexWrap:'wrap',left:'10vw'}}>
      <img
        src={data[item[0]]}
        alt={item[1].toFixed(3)}
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
      <p style={{position:'absolute',bottom:'290px', left:'90px'}}>{item[1].toFixed(3)}%</p>
    </div>
  ));
    return (
      <>
        {currentItems && imageElmt}
      </>
    );
  }

function PaginatedItems({ itemsPerPage, items, data}) {

    const [itemOffset, setItemOffset] = useState(0);
   
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    const currentItems = items.slice(itemOffset,endOffset);
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
          <div style={{display:'flex', position:'relative'}}>
          <Items currentItems={currentItems} data={data}/>
          </div>
          <div style={{position:'absolute',top:'435px',left:'220px'}}>
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





export default Search;
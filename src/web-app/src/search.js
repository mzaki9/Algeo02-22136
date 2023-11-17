import React, { useRef, useState } from 'react';
import ReactPaginate from 'react-paginate';
import './App.css'
import './import.css'

function Search(){
    const [SwitchVal, setSwitchVal] = useState(1); 
    const [timeExec, setTimeExec] = useState(0);
    const [tupleList, setTupleList] = useState([]);
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
             
    
            }catch(error){
                console.log('Error request to API',error)
            }
        }
    };
    const handleSwitchClick = ()=>{ // switch CBIR mode
        setSwitchVal(SwitchVal*-1);
        console.log(SwitchVal);
    };
    return(
        <div>
            <div style={{position:'relative', bottom:'25vh', right:'38vw'}}>
                <h3>
                    Switch CBIR mode:
                </h3>
            <button onClick={handleSwitchClick} > Switch </button>
            </div>

            <button  onClick={searchImg} className="searchButton"style={{position:'relative',bottom:'60vh', fontSize:'6vh'}}>
                SEARCH
            </button>
            <h3 style={{position:'relative',bottom:'42vh',color:'white',fontSize:'4vh', left:'35vw'}}>
              time: {timeExec} s
            </h3>
            {tupleList.length >1 && ( // Conditionally render only if tupleList has data
                <PaginatedItems itemsPerPage={2} items={tupleList} />
              )}
        </div>
    );
}
function Items({ currentItems}) {
  console.log(currentItems);

  const imageElmt = currentItems.map((item, index) => (
    <div key={index}>
      <img
        src={'../DataSet/' + item[0]}
        style={{
          position: 'relative',
          bottom: '30vh',
          minHeight: '200px',
          minWidth: '200px',
          maxHeight: '280px',
          maxWidth: '280px',
          marginRight: '40px', // Add some space between images
        }}
      />
      <p> {item[1]}</p>
    </div>
  ));
    return (
      <>
        {currentItems && imageElmt}
      </>
    );
}

function PaginatedItems({ itemsPerPage, items}) {
    // Here we use item offsets; we could also use page offsets
    // following the API or data you're working with.
    const [itemOffset, setItemOffset] = useState(0);
    // Simulate fetching items from another resources.
    // (This could be items from props; or items loaded in a local state
    // from an API endpoint with useEffect and useState)
    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    const currentItems = items.slice(itemOffset,endOffset);
    const pageCount = Math.ceil(items.length / itemsPerPage);
  
    // Invoke when user click to request another page.
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
          <div style={{position:'absolute',top:'45vh',left:'0vw'}}>
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
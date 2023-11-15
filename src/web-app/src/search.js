import React, { useRef, useState } from 'react';

function Search(){
    const [SwitchVal, setSwitchVal] = useState(1); 
    const [timeExec, setTimeExec] = useState(0);
    const [tupleList, setTupleList] = useState([]);
    const [jSonVal, setJSonVal] = useState(null);

    const searchImg = async ()=>{
        if (SwitchVal==1){
            console.log("CBIR texture");
            try{
                const response = await fetch('http://localhost:5000/cbirtexture',{
                    method:'GET',
                });
                const jsonData = await response.json();
                setJSonVal(jsonData);
                console.log(jSonVal);
    
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
                setJSonVal(jsonData);
                console.log(jSonVal);
    
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

            <button  onClick={searchImg } style={{position:'relative',bottom:'33vh', fontSize:'6vh'}}>
                SEARCH
            </button>
            <h3 style={{position:'relative',left:'30vw',bottom:'32vh',color:'white',fontSize:'3vh'}}>
              (time: Undefined yet)
            </h3>

        </div>
    );
}
export default Search;
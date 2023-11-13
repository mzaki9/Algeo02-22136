import './App.css';
import './ImageUpload'
import InputBox from './inputBox';
import DataSetBox from './dataSetBox';

function App() {
  return (
      <div className="App-header">
        <div className="HeadTab">
            <button id="ButtonHead1"> About us</button>
            <button id="ButtonHead2">camera</button>
            <button id="ButtonHead3">help</button>
        </div>
        <h2 style={{position:'relative',right:'35vw',top:'40vh',color:'white',fontSize:'4vh'}}>
        Input The Image</h2>
        <div  className="boxInputImage">
          <InputBox>
          </InputBox>
        </div>
        <h2 style={{position:'relative',left:'0vw',top:'70vh',color:'white',fontSize:'4vh'}}> Input The Data Set</h2>
          <DataSetBox/>
        <div className="resultBox">
          <h3 style={{position:'relative',left:'35vw',bottom:'12vh',color:'white',fontSize:'3vh'}}>
              (time: Undefined yet)
          </h3>
          <h3 style={{position:'relative',right:'40vw',bottom:'20vh',color:'white',fontSize:'4vh'}}>
              The Result
          </h3>
        </div>
      </div>
  );
}

export default App;

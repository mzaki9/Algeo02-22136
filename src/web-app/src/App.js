import './App.css';
import './ImageUpload'
import InputBox from './inputBox';
import DataSetBox from './dataSetBox';
import Search from './search';

function App() {
  return (
      <div className="App-header">
        <div className="HeadTab">
            <button id="ButtonHead1">Home</button>
            <button id="ButtonHead2">Camera: Off</button>
            <button id="ButtonHead3">About Us</button>
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
            <Search/>
        </div>
      </div>
  );
}

export default App;

import './App.css';
import './ImageUpload'
import ImageUpload from './ImageUpload';
import InputBox from './inputBox';
function App() {
  return (
      <div className="App-header">
      <div className="HeadTab">
          <button id="ButtonHead1"> About us</button>
          <button id="ButtonHead2">camera</button>
          <button id="ButtonHead3">help</button>
      </div>
      <div className="boxResult">
      </div>
      <InputBox/>
      </div>
  );
}

export default App;

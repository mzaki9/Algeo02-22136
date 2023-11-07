import logo from './logo.svg';
import './App.css';
import './ImageUpload'
import ImageUpload from './ImageUpload';
function App() {
  return (
    <div className="App" >
      <div className="HeadTab">
          <button id="ButtonHead1"> About us</button>
          <button id="ButtonHead2">camera</button>
          <button id="ButtonHead3">help</button>
      </div>
      <header className="App-header">
        <h1 class="Title">Sistem Temu Balik Gambar</h1>
        <div class="boxInputImage">
          <p>ceritanya gambar input</p>
        </div>
        <div class="uploadImageButton">
          <div>
          <ImageUpload></ImageUpload>
          </div>

        </div>
       <div class="boxResult">
          <p>hasil</p>
       </div>
      </header>
    </div>
  );
}

export default App;

import React from 'react';
import image1 from './image/image1.jpg';
import image2 from './image/image2.jpg';
import image3 from './image/image3.jpg';
import './aboutUs.css'; 

function AboutUs() {
  return (
    <div className="aboutUsContainer">
      <div className="aboutUsItem">
        <img src={image1} alt="Image 1" className="aboutUsImage" />
        <div className="aboutUsText">
          <h2>Muhammad Zaki</h2>
          <p>NIM : 13522136</p>
          <p>PESAN/KESAN : BANG UDAH BANG.</p>
        </div>
      </div>
      <div className="aboutUsItem">
        <img src={image2} alt="Image 2" className="aboutUsImage" />
        <div className="aboutUsText">
          <h2>Albert Ghazaly</h2>
          <p>NIM: 13522150</p>
          <p>PESAN/KESAN : أريد أن أنام دون التفكير في المهام</p>
        </div>
      </div>
      <div className="aboutUsItem">
        <img src={image3} alt="Image 3" className="aboutUsImage" />
        <div className="aboutUsText">
          <h2>About Image 3</h2>
          <p>isi aja bang.</p>
        </div>
      </div>
    </div>
  );
}

export default AboutUs;

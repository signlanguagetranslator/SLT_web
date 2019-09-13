import React from "react";
import Webcam from "react-webcam";
import './Webcam.css';

const IMAGE_SIZE = 227;

class Component extends React.Component {
  render() {
    // const videoConstraints = {
    //  width : 227,
    //  height : 227,
    //  facingMode : "user"
    // };

    return (
      <div className= "cam">
        <Webcam
        />;
      </div>
    );
  }
}

export default Webcam;

import React, { Component } from "react";
import "./App.css";
import Webcam from 'react-webcam'




class App extends Component {
  constructor(props){
    super(props);
    this.state =  {
      result: null,
      count: 0
    }
    this.url = 'http://localhost:5000/Wakeword';
    this.webcamRef = React.createRef(null);
    this.capture = this.capture.bind(this);
    this.videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: "user"
    };
     
   
  }

  capture() {
      console.log("Asdf");
      const imageSrc = this.webcamRef.current.getScreenshot();
      fetch(this.url, {
        method: 'POST',
        body: JSON.stringify({
          image: imageSrc
        }),
        headers: {
          "Content-type": "application/json"
        }
      }).then(response => response.json())
      .then( (responseData)=>{
            if(responseData.result) this.count++; 
            this.setState({
              result: responseData.result
            })
            console.log(this.count);
            console.log(responseData)
            return responseData
          }  
      );
    };

  render() {
    console.log(this.capture)
    return (
      <div className="App">
      <div id ="left" class="split-left">
        <h1> Camera </h1>
        <div className= "cam">
          <Webcam
          audio={false}
          height={500}
          ref={this.webcamRef}
          screenshotFormat="image/jpeg"
          width={450}
          videoConstraints={this.videoConstraints}/>
          <a>{this.state.result}</a><br/>
          <button onClick={this.capture}>Capture photo</button>
        </div>
      </div>
      <div id ="middle" class="split-middle">
        <h1> You say </h1>
      </div>
      <div class="split-right">
        <h1> Alexa says </h1>
      </div>
    </div>
    );
  }
}
 
export default App;
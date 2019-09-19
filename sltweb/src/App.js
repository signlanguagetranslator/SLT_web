import React, { Component } from "react";
import "./App.css";
import Webcam from 'react-webcam'

class App extends Component {
  constructor(props){
    super(props);
    this.state =  {
      state: 'Wakeword',
      Me : 'Wake me up',
      MeState: 'Waiting',
      AI : 'Wait for Wake',
      count : 0,
      sentence : ""
    }
    this.url = 'http://localhost:5000';
    this.webcamRef = React.createRef(null);
    this.buttonClick = this.buttonClick.bind(this);
    this.videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: "user"
    };
  }

  buttonClick(){
    console.log("Click " + this.state.state);
    if( this.state.state == 'Wakeword') this.Wakeword();
    else if ( this.state.state == 'SaveImage') this.SaveImage();
    else if (this.state.state == 'Predict') this.Predict();
  }

  Wakeword() {
    clearInterval(this.interval);
    const imageSrc = this.webcamRef.current.getScreenshot();
    fetch(this.url+"/Wakeword", {
      method: 'POST',
      body: JSON.stringify({
        image: imageSrc
      }),
      headers: {
        "Content-type": "application/json"
      }
    }).then(response => response.json())
    .then( (responseData)=>{
          if(responseData.result) this.setState({count: this.state.count++}); 
          if(responseData.result == "b'start\\n'")
            this.setState({MeState: "Recognizing",state: 'SaveImage',count : 0});
          else if(responseData.result == "b'finish\\n'"){
            this.loader.style.display = "block";
            this.setState({
              count : 0,
              MeState: "ASKING"
            });
            // action 
            // fetch dialogflow
            fetch(this.url+"/Dialogflow", {
              method: 'POST',
              body: JSON.stringify({
                sentence: this.state.sentence
              }),
              headers: {
                "Content-type": "application/json"
              }
            }).then(response => response.json())
            .then( (responseData)=>{
              //
            })
          }  
        this.interval = setInterval(this.buttonClick, 100);
      });
  };

  SaveImage() {
    clearInterval(this.interval);
    const imageSrc = this.webcamRef.current.getScreenshot();
    this.setState({
      count: this.state.count+1
    })
    fetch(this.url + "/SaveImage", {
      method: 'POST',
      body: JSON.stringify({
        image: imageSrc,
        fileName: this.state.count
      }),
      headers: {
        "Content-type": "application/json"
      }
    }).then( ()=> {
        if( this.state.count == 25 ){
          this.setState({
            state : 'Predict'
          });
        }
        this.interval = setInterval(this.buttonClick, 100); 
      }
    )
  };

  Predict() {
    clearInterval(this.interval);
    const imageSrc = this.webcamRef.current.getScreenshot();
    fetch(this.url + "/Predict", {
      method: 'GET',
      headers: {
        "Content-type": "application/json"
      }
    }).then(response => response.json())
    .then( (responseData)=>{
        this.setState({
          state: 'Wakeword',
          count: 0,
          sentence : this.state.sentence + " " + responseData.word
        })
        this.interval = setInterval(this.buttonClick, 100);
      }
    );
  };

  render() {
    return (
      <div className="App">
      <div id ="left" class="split-left">
        <h1> Camera </h1>
        <div className= "cam">
          <Webcam
          audio={false}
          height={500}
          width={450}
          ref={this.webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={this.videoConstraints}/>
          <a>{this.state.result}</a><br/>
        </div>
      </div>
      <div id ="middle" class="split-middle">
        <h1>You</h1>
        { this.state.state == "Wakeword" ? <h1 style={{background: 'black', color: 'white'}}> Waiting </h1> : null}
        { this.state.state == "SaveImage" ? <div><h1 style={{background: 'red', color: 'white'}}>Recoding</h1> <h1 style={{background: 'red', color: 'white'}}>Frame : {this.state.count}</h1></div> : null}
        { this.state.state == "Predict" ? <h1 style={{background: 'green', color: 'white'}}> Recognizing </h1> : null}
        <h1>{this.state.sentence}</h1>
      </div>
      <div class="split-right">
        <h1> Alexa says </h1>
        <div id="loader"></div>
      </div>
    </div>
    );
  }
  componentDidMount(){
    this.interval = setInterval(this.buttonClick, 100);
    setTimeout(this.interval, 3000); // Here
    this.loader = document.getElementById("loader")
    
  }
}
export default App;
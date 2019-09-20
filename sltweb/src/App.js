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
      AI : null,
      count : 0,
      sentence : "",
      delay: null
    }
    this.emotion = "";
    this.url = 'http://localhost:5000';
    this.webcamRef = React.createRef(null);
    this.buttonClick = this.buttonClick.bind(this);
    this.videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: "user"
    };
    this.setState = this.setState.bind(this)
  }

  buttonClick(){
    console.log("Click " + this.state.state);
    if( this.state.state === 'Wakeword') this.Wakeword();
    else if ( this.state.state === 'SaveImage') this.SaveImage();
    else if (this.state.state === 'Predict') this.Predict();
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
          if(responseData.result === "b'start\\n'"){
            this.interval = setInterval(this.buttonClick, 60);
            if (this.emotion == null ){
              this.setState({MeState: "Recognizing",state: 'SaveImage',count : 0, sentence: "",delay: null});
            } else this.setState({MeState: "Recognizing",state: 'SaveImage',count : 0,delay: null});
          }
          else if(responseData.result === "b'finish\\n'"){
            this.loader.style.display = "block";
            this.setState({
              count : 0,
              MeState: "ASKING"
            });
            fetch(this.url+"/Chat", {
              method: 'POST',
              body: JSON.stringify({
                sentence: this.state.sentence,
                emotion : this.emotion
              }),
              headers: {
                "Content-type": "application/json"
              }
            }).then(response => response.json())
            .then( (responseData)=>{
              this.setState({
                AI: responseData.response,
              });
              this.emotion = null;
              this.interval = setInterval(this.buttonClick, 300);
            })  
          } else{
            this.interval = setInterval(this.buttonClick, 300);
          }
      });
  };

  SaveImage() { 
    if(this.state.count > 25) return;
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
        if( this.state.count >= 25 ){
          this.setState({
            state : 'Predict'
          });
        }
      }
    )
  };

  Predict() {
    clearInterval(this.interval);
    fetch(this.url + "/Predict", {
      method: 'POST',
      body: JSON.stringify({
        emotion: this.emotion
      }),
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
        this.emotion = responseData.emotion;
        this.interval = setInterval(this.buttonClick, 300);
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
        </div>
      </div>
      <div id ="middle" class="split-middle">
        <h1>You</h1>
        { this.state.state === "Wakeword" ? <h1 style={{background: 'black', color: 'white'}}> Waiting </h1> : null}
        { this.state.delay !== null ? <h1 style={{background: 'black', color: 'white'}}>{this.state.delay} </h1> : null}
        { this.state.state === "SaveImage" ? <div><h1 style={{background: 'red', color: 'white'}}>Recoding</h1> <h1 style={{background: 'red', color: 'white'}}>Frame : {this.state.count}</h1></div> : null}
        { this.state.state === "Predict" ? <h1 style={{background: 'green', color: 'white'}}> Recognizing </h1> : null}
        <h1>{this.state.sentence}</h1>
        <h1>{this.emotion}</h1>
      </div>
      <div class="split-right">
          <h1> AI </h1>
          {this.state.AI == null ? <div id="loader"></div>:<h1 style={{background: 'blue', color: 'white'}}>{this.state.AI}</h1>}
      </div>
    </div>
    );
  }
  componentDidMount(){
    this.interval = setInterval(this.buttonClick, 500);
    this.loader = document.getElementById("loader")
  }
}
export default App;
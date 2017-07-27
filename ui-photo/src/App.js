import React, { Component } from 'react';
import './App.css';
import AppStore from './AppStore';
import {ButtonToolbar, Button, Grid, Row, Col, Image} from 'react-bootstrap';

class App extends Component {
  constructor(){
    super();
    this.state = {
      button_state: null,
      image: null,
      countdown: null,
    }  
  }
  
  componentWillMount() {
        AppStore.on("get_button", () => {
          console.log("button state")
            this.setState({
                button_state: AppStore.getButtonState(),
            })
        })
        AppStore.on("get_image", () => {
          console.log("image state")
            this.setState({
                image: AppStore.getImage(),
            })
        })
        AppStore.on("get_countdown", () => {
           var count = AppStore.getCountdown()
           if(count.nb===0){
             count = null
           }
           this.setState({
                 countdown: count,
           })
        })
    }
    
  render() {
    
    // <Image className="Iimg" href="#" alt="171x180" src="mariages-background.jpg" thumbnail />
    let img = <Col></Col>
    
	if(this.state.image != null){
      console.log(this.state.image.photo_raw)
      if(this.state.image.photo_raw === "mariages-background.jpg"){
		img = <Col></Col>
	  } else {
        img = <Col><Image className="Iimg" href="#" alt="171x180" src={this.state.image.photo_raw} thumbnail /></Col>
	  }
    }
    
    let buttons = <div className="Bar-Button">
          <ButtonToolbar>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Photo classique</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Photo noir & blanc</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Photo'maton</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Photo message</Button>
          </ButtonToolbar>
         </div>


    if(this.state.button_state != null){
      if(this.state.button_state.diplay_texte === true){
        buttons = <div className="Bar-Button">
          <ButtonToolbar>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 250 }} bsSize="large">Une journée inoubliable !</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 250 }} bsSize="large">Un souvenir du mariage</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Merci la vie !</Button>
            <Button style={{ backgroundColor:"#808080", marginRight: 60, width: 200 }} bsSize="large">Vive les mariés !</Button>
          </ButtonToolbar>
         </div>
      }
    } 

    // let count = <p></p>
    // if(this.state.countdown != null){
    //  count = <p>{this.state.countdown.nb}</p>
    // }
    
    // <Col md={ 2 }> {count} </Col>
    return (
      <div className="App">
        <div>
          <Grid>
            <Row className="Line-Row">
            <Col md={10}>
              {img}
            </Col>
            </Row>
          </Grid>
        </div>
        {buttons}
      </div>
    );
  }
}

export default App;

import { EventEmitter } from "events";

class AppStore extends EventEmitter {
    constructor() {
        super();
        
        this.button_state = {}
        this.images = {}
        this.countdown = {}
        this.connectWebSocket = this.connectWebSocket.bind(this);
        this.connectWebSocket()
    }

    connectWebSocket(){
        this.ws = new WebSocket('ws://localhost:8000/');
        console.log("websocket", this.ws)
        this.ws.onmessage = this.handleData.bind(this);
    }
    
    handleData(data) {
        var message = JSON.parse(data.data);
        console.log(message)
        if(message['type']==='button_state'){
            this.button_state = message;
            this.emit("get_button");
        } else if(message['type']==='countdown'){
            this.countdown = message; 
            this.emit("get_countdown")
        } else {
            this.images = message;
            this.emit("get_image");
        }
    }
    
    getButtonState(){
        return this.button_state
    }
    
    getImage(){
        return this.images
    }

    getCountdown(){
        return this.countdown
    }
}


const appStore = new AppStore();

export default appStore;

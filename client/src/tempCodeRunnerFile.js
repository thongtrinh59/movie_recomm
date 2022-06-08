import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import './static/css/chat_interface.css';
import './static/css/temporary.css';

class SendButton extends Component{
    render(){
      return (<div className="send_message" onClick={this.props.handleClick}>
                <div className="text">send</div>
              </div>);
    }
}

class MessageTextBoxContainer extends Component{
  render(){
    return(
      <div className="message_input_wrapper">
        <input id="msg_input" className="message_input" placeholder="Type your messages here..." value={this.props.message} onChange={this.props.onChange} onKeyPress={this.props._handleKeyPress}/>
      </div>
    );
  }
}

class Avartar extends Component {
  render(){
    return(
      <div className="avatar"/>
    );
  }
}

class BotMessageBox extends Component{
  constructor(props) {
    super(props);
  }
  render(){
    return(
      <li className="message left appeared">
        <Avartar></Avartar>
        <div className="text_wrapper">
            <div className="text">{this.props.message}</div>
        </div>
      </li>
    );
  }
}

class UserMessageBox extends Component{
  constructor(props) {
    super(props);

  }
  render(){
    return(
      <li className={`message ${this.props.appearance} appeared`}>
        <Avartar></Avartar>
        <div className="text_wrapper">
            <div className="text">{this.props.message3}</div>
        </div>
      </li>
    );
  }
}


class SecondUserMessageBox extends Component{
  constructor(props) {
    super(props);

  }
  render(){
    return(
      <div class='moviescrollbar'> 
        <a href='https://www.imdb.com/title/tt0387564' target='_blank'>
          <div class='movie-box'>
            <img src='http://img.omdbapi.com/?apikey=ea75cc5f&i=tt0387564'/>
            <p class='movie-title'>Saw</p>
            <p class='movie-details'>103.0 • 2004-10-01 • IMBD: 7.2</p>
          </div>
        </a>  
      </div>
    );
  }
}



class MessagesContainer extends Component{
  constructor(props) {
    super(props);
    this.createBotMessages = this.createBotMessages.bind(this);
  }

  scrollToBottom = () => {
    var el = this.refs.scroll;
    el.scrollTop = el.scrollHeight;
  }

  componentDidMount() {
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  createBotMessages(){
    console.log(this.props.messages);

    return this.props.messages.map((message, index) =>
      <UserMessageBox key={index} message3={message["message"]} appearance={message["isbotmessage"] ? "left": "right"}/>
    );
    
  }

  render(){

    return(
      <ul className="messages" ref="scroll">
        {this.createBotMessages()}
      </ul>
    );
  }
}

class Movieshows extends Component{
  constructor(props) {
    super(props);
  }

  
  // var temp2 = temp.map(item => item.split("++++"))
  render(){
    var tuiti = this.props.message;
    console.log(this.props.messages);
    return(
      <div class='moviescrollbar'> 
        <a href='https://www.imdb.com/title/tt0387564' target='_blank'>
          <div class='movie-box'>
            <img src='http://img.omdbapi.com/?apikey=ea75cc5f&i=tt0387564'/>
            <p class='movie-title'>{tuiti}</p>
            <p class='movie-details'>{tuiti}</p>
          </div>
        </a>  
        
      </div>
    );
  }
}


class ChatApp extends Component {
  constructor(props){
    super(props);
    this.state = {"messages": [], "current_message":"", temp: true }
    this.handleClick = this.handleClick.bind(this);
    this._handleKeyPress = this._handleKeyPress.bind(this);
    this.onChange = this.onChange.bind(this);
    this.addMessageBox = this.addMessageBox.bind(this);
  }
  

  addMessageBox(enter=true){
    let messages = this.state.messages;
    let current_message = this.state.current_message;
    console.log(this.state);
    if(current_message && enter){
      messages = [...messages, {"message":current_message}];
      fetch("http://localhost:5000?message=" + current_message)
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result);
          var outpmess = result["type"]
          if (outpmess === "mess1") {
            this.setState({ temp: true });
            let output = ''
            result["message"].forEach(element => {
              output += element;
            });
            // output += outpmess
            this.setState({
              messages: [...messages, {"message":output, "isbotmessage":true}]
            });
          } else if (outpmess === "mess2") {
            this.setState({ temp: false });
            // this.setState({
            //   // messages: [...messages, output]
            //   temp: false,
            //   messages: [...messages, {"message":["saw", "horror"],"isbotmessage":true} ]
            // });
            // let output = ''
            // result["message"].forEach(element => {
            //   output += element;
            // });
            // // output += outpmess
            // this.setState({
            //   messages: [...messages, {"message":output, "isbotmessage":true}]
            // });
            
          }
          

          // this.setState({
          //   messages: [...messages, {"message":result["message"], "isbotmessage":true}]
          // });
        },
        (error) => {
          //do nothing for now
        }
      );
      current_message = ""
    }  
    this.setState({
      current_message: current_message,
      messages
    });

  }

  handleClick(){
    this.addMessageBox();
  }

  onChange(e) {
    this.setState({
      current_message: e.target.value
    });  
  }

    _handleKeyPress(e) {
    let enter_pressed = false;
    if(e.key === "Enter"){
      enter_pressed = true;
    }
    this.addMessageBox(enter_pressed)
  }

  render() {
    let meg
    if (this.state.temp) {
      meg = <MessagesContainer messages={this.state.messages}></MessagesContainer>
    } else {
      meg = <Movieshows messages={this.state.messages}></Movieshows>
    }

    return (
      <div className="chat_window">
        {meg}
        <div className="bottom_wrapper clearfix">
          <MessageTextBoxContainer 
            _handleKeyPress={this._handleKeyPress} 
            onChange={this.onChange} 
            message={this.state.current_message}></MessageTextBoxContainer>
          <SendButton handleClick={this.handleClick}></SendButton>
        </div>
        
      </div>
    );
  }
}



export default ChatApp;

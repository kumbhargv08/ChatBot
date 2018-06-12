import React, { Component } from 'react';
import ChatMessage from './ChatMessage.js'
import './App.css';
import ChatBot from 'react-simple-chatbot';
import TextToSpeech from './TextToSpeech';

const withTextToSpeech = [
  {
    id: '1',
    component: <TextToSpeech msg="Hi" />,
    trigger: '2',
  },
  {
    id: '2',
    user: true,
    trigger: '3',
  },
  {
    id: '3',
    component: <TextToSpeech msg='What is your name?' />,
    trigger: '4',
  },
  {
    id: '4',
    user: true,
    trigger: '5',
  },
  {
    id: '5',
    component: <TextToSpeech msg = 'Nice to meet you!' />,
    trigger: 6,
  },
  {
    id: '6',
    component: <TextToSpeech msg='How can i help you?' />,
    trigger: 'search',
  },
  {
    id: 'search',
    user: true,
    trigger: '7',
  },
  {
    id: '7',
    component: <ChatMessage />,
    waitAction: true,
    trigger: 'search',
  },
]

const withoutTextToSpeech = [
  {
    id: '1',
    message: 'hi',
    trigger: '2',
  },
  {
    id: '2',
    user: true,
    trigger: '3',
  },
  {
    id: '3',
    message: 'What is your name?',
    trigger: '4',
  },
  {
    id: '4',
    user: true,
    trigger: '5',
  },
  {
    id: '5',
    message: 'Hi {previousValue}, nice to meet you!',
    trigger: 6,
  },
  {
    id: '6',
    message: 'How can i help you?',
    trigger: 'search',
  },
  {
    id: 'search',
    user: true,
    trigger: '7',
  },
  {
    id: '7',
    component: <ChatMessage />,
    waitAction: true,
    trigger: 'search',
  },
]



class App extends Component {

  constructor( props ){
    super( props )
    this.state= {
      textToSpeech: true,
      steps : withTextToSpeech 
    }
  }
  render() {
    console.log(this.state.textToSpeech)
    return (
      <div className="App">
      <button onClick={() => this.setState({textToSpeech: !this.state.textToSpeech})}>Mute</button>
        <ChatBot
          headerTitle="PP ChatBot"
          recognitionEnable={true}
          steps={this.state.textToSpeech ? withTextToSpeech : withoutTextToSpeech}
        />
      </div>
    );
  }
}

export default App;

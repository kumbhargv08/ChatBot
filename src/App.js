import React, { Component } from 'react';
import ChatMessage from './ChatMessage.js'
import './App.css';
import ChatBot from 'react-simple-chatbot';


class App extends Component {

  constructor( props ){
    super( props )
    this.state= {
      steps : [
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
          trigger: '6',
        },
      ]
    }
  }
  render() {
    return (
      <div className="App">
        <ChatBot
          headerTitle="PP ChatBot"
          recognitionEnable={true}
          steps={this.state.steps}
        />
      </div>
    );
  }
}

export default App;

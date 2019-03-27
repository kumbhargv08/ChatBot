import React, { Component } from 'react';
import ChatMessage from './ChatMessage.js'
import './App.css';
import ChatBot from 'react-simple-chatbot';
import TextToSpeech from './TextToSpeech';
import v4 from 'uuid/v4';
import ChatBotHeader from './Header'

let withTextToSpeech = [
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
    component: <TextToSpeech msg='Nice to meet you!' />,
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
  }
]

let withoutTextToSpeech = [
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
  }
]



class App extends Component {

  constructor(props) {
    super(props)
    const sessionId = v4(),
      ChatMessageElement = {
        id: '7',
        component: <ChatMessage sessionId={sessionId} />,
        waitAction: true,
        trigger: 'search',
      }

    this.state = {
      textToSpeech: true,
      steps: withTextToSpeech,
      sessionId: sessionId
    }
    withTextToSpeech.push(ChatMessageElement)
    withoutTextToSpeech.push(ChatMessageElement)
  }

  render() {
    console.log(this.state.textToSpeech)
    return (
      <div className="App">
        {/* <button onClick={() => this.setState({textToSpeech: !this.state.textToSpeech})}>Mute</button> */}
        <ChatBot
          headerTitle="ChatBot"
          recognitionEnable={true}
          steps={this.state.textToSpeech ? withTextToSpeech : withoutTextToSpeech}
          enableMobileAutoFocus={true}
          headerComponent={<ChatBotHeader />}
          botAvatar='./avatar.svg'
        />
      </div>
    );
  }
}

export default App;

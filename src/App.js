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

    this.state = {
      textToSpeech: true,
      steps: withTextToSpeech,
      sessionId: v4(),
      category: 'HL',
      lendToken: '',
    }

    this.handleCategoryClick = this.handleCategoryClick.bind(this)
    this.getChatElement = this.getChatElement.bind(this)
  }

  componentDidMount() {
    let url = 'https://erpuat.ltfs.com:446/LTFSPerfiosApp/api/twhlLogin';
    // can do service call here to get response and set response t result

    axios({
      method: 'post',
      url: url,
      data: {
        "registrationToken": "dDkU_gCL_u4:APA91bGGtCdVvOlX1fVMrI-y5h_D_Xv4kdWjWQgvs5Vh03m-G7FYfmSnZafeedOa5UHFOqhClkJYExFowDJNl6bLh4m0fDlCdg-tL1lOG4q1am4tocreeBDdSy7IM78ztcudODhyubqc",
        "passWord": "welcome@1234", "userName": "USERHL11",
        "imei": "869737024563196", "partnerFlag": "false", "product": "TW", "version": "12.1.5"
      },
    }).then(function (response) {
      console.log('' + response);
      let token = response.data.token

      this.setState({ lendToken: token })
    })
      .catch(function (error) {
        console.log(error);
        self.setState({ loading: false, result: errorResponse })
      });
  }

  componentWillMount() {
    const ChatMessageElement = {
      id: '7',
      component: <ChatMessage
        sessionId={this.state.sessionId}
        category={this.state.category}
        lendToken={this.state.lendToken}
      />,
      waitAction: true,
      trigger: 'search',
    }
    withTextToSpeech.push(ChatMessageElement)
    withoutTextToSpeech.push(ChatMessageElement)
  }

  getChatElement(value) {
    const ChatMessageElement = {
      id: '7',
      component: <ChatMessage
        sessionId={this.state.sessionId}
        category={value}
        lendToken={this.state.lendToken}
      />,
      waitAction: true,
      trigger: 'search',
    }
    withTextToSpeech.pop()
    withoutTextToSpeech.pop()
    withTextToSpeech.push(ChatMessageElement)
    withoutTextToSpeech.push(ChatMessageElement)
    console.log(withTextToSpeech, withoutTextToSpeech, ChatMessageElement, 'hahahaha')
  }

  handleCategoryClick(value) {
    this.setState({ category: value })
    this.getChatElement(value)
  }

  render() {
    console.log(this.state)
    return (
      <div className="App">
        {/* <button onClick={() => this.setState({textToSpeech: !this.state.textToSpeech})}>Mute</button> */}
        <ChatBot
          headerTitle="ChatBot"
          recognitionEnable={true}
          steps={this.state.textToSpeech ? withTextToSpeech : withoutTextToSpeech}
          enableMobileAutoFocus={true}
          headerComponent={
            <ChatBotHeader
              handleClick={(value) => this.handleCategoryClick(value)}
            />}
          botAvatar='./avatar.svg'
        />
      </div>
    );
  }
}

export default App;

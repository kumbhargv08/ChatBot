import React, { Component } from 'react';
import { Loading } from 'react-simple-chatbot';
import './App.css';
import axios from 'axios';
import { TextToSpeech } from './TextToSpeech';

class ChatMessage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      result: '',
      trigger: false
    };

    this.triggetNext = this.triggetNext.bind(this);
  }

  componentWillMount() {
    const self = this;
    const { steps, sessionId } = this.props;
    const search = steps.search.value + ' % ' + this.props.category;
    const errorResponse = 'do you want to raise a ticket for this request'
    if (search.toLowerCase().trim() != 'bye' && !search.toLowerCase().trim().startsWith('#reason')) {
      let url = 'http://localhost:5000/userQuery';

      // can do service call here to get response and set response t result

      axios({
        method: 'post',
        url: url,
        data: {
          query: search,
          sessionId: sessionId
        }
      }).then(function (response) {
        //console.log( '' + response );
        let answer = response.data ? response.data.answer : errorResponse;
        answer = answer.replace(/-/g, "")
        //answer = ( answer.__contains__('I am sorry, but I do not understand') ) ? answer = answer.replace('I am sorry, but I do not understand',errorResponse): answer
        console.log(answer);
        self.setState({ loading: false, result: answer })
      })
        .catch(function (error) {
          console.log(error);
          self.setState({ loading: false, result: errorResponse })
        });
    } else if (search.toLowerCase().trim().startsWith('#reason')) {
      let url = 'https://erpuat.ltfs.com:446/LTFSPerfiosApp/api/PopulateTWHL';
      let appId = search.toLowerCase().trim().split(':')(1)
      // can do service call here to get response and set response t result

      axios({
        method: 'post',
        url: url,
        data: {
          appId: appId,
          includeLoans: true,
          getQtns: false,
          getbanks: false
        },
        headers: { lendToken: this.props.lendToken }
      }).then(function (response) {
        console.log('' + response);
        let answer = response.data.BRE_Rejection_Reason__c;
        answer = answer.replace(/-/g, "")
        //answer = ( answer.__contains__('I am sorry, but I do not understand') ) ? answer = answer.replace('I am sorry, but I do not understand',errorResponse): answer
        console.log(answer);
        self.setState({ loading: false, result: answer })
      })
        .catch(function (error) {
          console.log(error);
          self.setState({ loading: false, result: errorResponse })
        });
    }
    else {
      self.setState({ loading: false, result: 'Bye, Have a nice day' })
    }
  }

  triggetNext() {
    this.setState({ trigger: true }, () => {
      this.props.triggerNextStep();
    });
  }

  render() {
    const { trigger, loading, result } = this.state;

    return (
      <div>
        {loading ? <Loading /> : <TextToSpeech msg={result} />}
        {
          !loading &&
          !trigger &&
          this.triggetNext()
        }
      </div>
    );
  }
}
export default ChatMessage;

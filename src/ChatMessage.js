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
      trigger: false,
    };

    this.triggetNext = this.triggetNext.bind(this);
  }

  componentWillMount() {
    const self = this;
    const { steps } = this.props;
    const search = steps.search.value;
    const errorResponse = 'sorry, I did not understand that. We have posted your query to pp slack channel'
    if( search.toLowerCase().trim() != 'bye') {
      let url = 'http://localhost:5000/chat/query/' + search;

      // can do service call here to get response and set response t result

      axios.get( url , {
        headers: {
          'Access-Control-Allow-Origin': '*',
        }
      })
        .then(function (response) {
          //console.log( '' + response );
          let answer = response.data ? response.data.answer : errorResponse;
          answer = answer.replace(/-/g,"")
          //answer = ( answer.__contains__('I am sorry, but I do not understand') ) ? answer = answer.replace('I am sorry, but I do not understand',errorResponse): answer
          console.log( answer );
          self.setState({ loading: false, result: answer })
        })
        .catch(function (error) {
          console.log(error);
          self.setState({ loading: false, result: errorResponse })
        });
      } else {
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
        { loading ? <Loading /> : <TextToSpeech msg={result} /> }
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

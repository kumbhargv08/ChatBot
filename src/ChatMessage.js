import React, { Component } from 'react';
import { Loading } from 'react-simple-chatbot';
import axios from 'axios'; 

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
    let url = 'http://localhost:5000/chat/query/' + search;

    // can do service call here to get response and set response t result
    axios.get( url , {
      headers: {
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(function (response) {
        let answer = response.data ? response.data.answer : 'sorry, we cant help you. Please contact Vidya';
        answer = answer.replace(/-/g,"")
        answer = ( answer == 'I am sorry, but I do not understand.' ) ? 'sorry, we cant help you. Please contact Vidya': answer
        console.log( answer );
        self.setState({ loading: false, result: answer })
      })
      .catch(function (error) {
        console.log(error);
        self.setState({ loading: false, result: 'sorry, we cant help you. Please contact Vidya' })
      });

    
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
        { loading ? <Loading /> : result }
        {
          !loading &&
          <div
            style={{
              textAlign: 'center',
              marginTop: 20,
            }}
          >
            {
              !trigger && this.triggetNext()
            }
          </div>
        }
      </div>
    );
  }
}
export default ChatMessage;

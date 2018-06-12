import React from 'react';
import Artyom from "artyom.js"


export class TextToSpeech extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            jarvis: new Artyom(),
        };   
    }
    
    componentDidMount() {
        this.state.jarvis.say(this.props.msg);
    }

    componentDidUpdate(prevProps) {
        if(prevProps.msg !== this.props.msg) {
            this.state.jarvis.say(this.props.msg);
        }
    }

    render() {
        return(
            <div>{this.props.msg}</div>
        )
    }
}

export default TextToSpeech;
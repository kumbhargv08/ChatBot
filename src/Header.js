import React from 'react'
import './App.css'
import logo from './lnt1.png'

class ChatBotHeader extends React.Component {
    render() {
        return (
            <div>
                <div className='header-style'>
                    <div style={{ textAlign: 'left' }} onClick={(e) => this.props.handleClick(e.target.value)}>
                        <select className='drop-down'>
                            <option value="HL">HL</option>
                            <option value="BL">BL</option>
                            <option value="Category3">Category3</option>
                            <option value="Category4">Category4</option>
                        </select>
                    </div>
                    <span>
                        <img src={logo} alt='Logo' className='logo-style'></img>
                    </span>
                </div>
            </div>
        )
    }

}

export default ChatBotHeader

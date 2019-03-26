import React from 'react'
import './App.css'
import logo from './larsen-and-tubro.png'
import Dropdown from 'react-bootstrap'

class ChatBotHeader extends React.Component {
    render() {
        return (
            <div>
                <div className='header-style'>
                    <div style={{textAlign:'left'}}>
                        <select className='drop-down'>
                            <option value="Category1">Category1</option>
                            <option value="Category2">Category2</option>
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

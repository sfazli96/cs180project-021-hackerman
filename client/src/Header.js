import React, { Component } from 'react'

class Header extends Component {

    render() {
        return (
            <div>
                <h2>This is the header</h2>
                <button onClick>Home page</button>
                <button onClick>Login</button>
            </div>
        )
    }
}

export default Header;


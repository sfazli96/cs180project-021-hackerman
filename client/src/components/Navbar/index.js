import React from 'react'
import {
    Nav, 
    NavLink, 
    Bars, 
    NavMenu, 
    NavBtn,
    NavBtnLink
    } from './NavbarElements';

const Navbar = () => {
    return (
        <div>
            <Nav>
                <NavLink to = "/home">
                    <h1>Youtube</h1>
                </NavLink>
                // <Bars> 

                // </Bars>
                <NavMenu>
                    <NavLink to = "/home" activeStyle> 
                        Home
                    </NavLink>
                    <NavLink to = "/US" activeStyle> 
                        United States
                    </NavLink>
                    <NavLink to = "World" activeStyle> 
                        World
                    </NavLink>
                </NavMenu>
            </Nav>
        </div>
    )
}

export default Navbar

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
                <NavLink to = "/">
                    <h1>Youtube</h1>
                </NavLink>
                <Bars> 

                </Bars>
                <NavMenu>
                    <NavLink to = "/home" activeStyle> 
                        Home
                    </NavLink>
                    <NavLink to = "/US" activeStyle> 
                        United States
                    </NavLink>
                    <NavLink to = "/contact-us" activeStyle> 
                        Contact Us
                    </NavLink>
                    <NavLink to = "World" activeStyle> 
                        World
                    </NavLink>
                    <NavBtnLink to='/InformationPage'>Information Page</NavBtnLink>
                </NavMenu>
                <NavBtn> 
                <NavBtnLink to='/signin'>Sign in</NavBtnLink>
                </NavBtn>
            </Nav>
        </div>
    )
}

export default Navbar

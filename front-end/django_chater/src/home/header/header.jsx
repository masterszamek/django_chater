import {Navbar, Nav} from 'react-bootstrap';
import React from "react";

import routing_urls from "home/routing_urls";

import NavLink from "_components/nav_link";
import NavSupportItem from "./nav_support_item";
import NavSettingsItem from "./nav_settings_item";



export default function Header(props){

    const authenticated = props.user.authenticated;
    return (

        <Navbar bg="dark" variant="dark" onSelect={(eventKey, event)=>{console.log(eventKey, event)}}>
            <Navbar.Brand>Szamex Chater</Navbar.Brand>

                <Nav className="mr-auto">
                    <NavLink to={routing_urls.home} >Home</NavLink>
                    {authenticated? <NavLink to={routing_urls.workspaces}>Workspaces</NavLink>: undefined}
                    <NavSupportItem/>

                </Nav>
                                
                {authenticated ? 
                   <Nav>
                       <Nav.Item className="nav-link">Logout</Nav.Item>
                       <NavSettingsItem></NavSettingsItem>
                   </Nav>
                 :
                    <Nav>
                        <NavLink to={routing_urls.sign_in}>Sign In</NavLink>
                        <NavLink to={routing_urls.sign_up}>Sign up</NavLink>
                    </Nav>
                }

        



        </Navbar>

      )
}
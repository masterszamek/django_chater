import React from "react";
import {Nav} from "react-bootstrap";
import {NavLink} from "react-router-dom";



const CustomNavLink = ({children, ...rest}) =>(
    <Nav.Item className="nav-link" exact={true} as={NavLink} {...rest} >{children}</Nav.Item>
)

export {CustomNavLink as default};
import React from 'react';
import { Nav, Dropdown } from 'react-bootstrap';
import {NavLink} from 'react-router-dom';


const NavDropdownItem = ({title, items, ...rest_props}) =>{

    return (
        <Dropdown  as={Nav.Item} {...rest_props} className="nav-link">
            <Dropdown.Toggle as={Nav.Item}>{title}</Dropdown.Toggle>

            <Dropdown.Menu className="dropdown_item_backgroud_color">
                {items.map((item, index)=> (
                    <Dropdown.Item as={NavLink} to={item.to} key={index}>{item.title}</Dropdown.Item>
                    
                ))}
            </Dropdown.Menu>

        </Dropdown>
    );

}


export {NavDropdownItem as default}
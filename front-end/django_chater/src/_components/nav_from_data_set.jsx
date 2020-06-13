import React from "react";
import NavLink from "./nav_link";
import {Nav} from 'react-bootstrap';


const NavFromDataSet = ({data}) =>(
/**
 * Generate Nav from data set
 * @param {data} list contain objetcs. 
 * Each object require:
 *      @param {to} str its link panth
 *      @param {title} str  its title Nav item
 *      optionaly @param {onClick} function perform onClick on NavItem
 */

    <Nav>
        {data.map((item, index)=>{
            if(item.onClick===undefined)
                return (
                    <NavLink key={index} to={item.to}>
                        {item.title}
                    </NavLink>
                )
            return(
                <NavLink key={index} to={item.to} onClick={()=>(item.onClick())}>
                    {item.title}
                </NavLink>
            )
        })}
    </Nav>

);

export {NavFromDataSet as default}


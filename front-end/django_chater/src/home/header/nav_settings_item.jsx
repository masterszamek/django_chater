import React from 'react';


import urls from "home/routing_urls";

import NavDropdownItem from "_components/nav_dropdown_item";


let items = [
    {
        to: urls.settings.change_password,
        title: "Change Password",
    }
]

const NavSettingstItem = (props)=><NavDropdownItem items={items} title="Support" alignRight></NavDropdownItem>


export {NavSettingstItem as default};

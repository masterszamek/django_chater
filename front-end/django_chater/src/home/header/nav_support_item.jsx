import React from 'react';

import urls from "home/routing_urls";

import NavDropdownItem from "_components/nav_dropdown_item";



let items = [
    {
        to: urls.support.about_me,
        title: "About me",
    },
    {
        to: urls.support.contact,
        title: "Contact",
    },
    {
        to: urls.support.ideas,
        title: "Ideas",
    },
]

const NavSupportItem = (props)=><NavDropdownItem items={items} title="Support"></NavDropdownItem>


export {NavSupportItem as default};

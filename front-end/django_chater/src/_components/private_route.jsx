import React from "react";
import { Route, Redirect } from "react-router";
import Authentication from "./../_services/auth_service.js";



const PrivateRoute = ({component:Component, ...args}) =>(
    <Route 
        {...args} 
        render = {(props) =>{
            const user =  Authentication.get_user;
            if (!user.authenticated)
                return <Redirect to={{pathname: '/login', state: {from: props.location}}}/>
            return <Component {...props}/>
            
        }}
    />    
);


export {PrivateRoute as default};
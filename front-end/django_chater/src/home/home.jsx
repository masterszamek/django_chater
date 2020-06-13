import React from "react";
import {Route, Switch} from 'react-router-dom';




import Header from "./header/header";

import "css/home/home.css";


import {Form, Button} from 'react-bootstrap';
class TestowyKomponent extends React.Component{
    render(){

        return(
        <Form onSubmit={ e => {e.preventDefault();    console.log(e);}}>
            <Form.Group controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" />
                <Form.Text className="text-muted">
                We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            <Form.Group controlId="formBasicCheckbox">
                <Form.Check type="checkbox" label="Check me out" />
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
    )}
}


export default function Home(props){
    console.log(props)
    const user = props.user;

    return (
        <>
        <Header user={user}/>
        <Switch>
            <Route render={(props)=>(<TestowyKomponent/>)}path="/" exact></Route>
            <Route path="/login/" exact> <div> A login page</div> </Route>
            <Route path="/sign_up" exact> <div> A sign up page</div> </Route>
            <Route path="/logout/" exact> <div> A logout page</div> </Route>
            <Route path="/settings/" exact> <div> A sssettings page</div> </Route>
            <Route path="/about/" exact> <div> A About page</div> </Route>
            <Route path="/support/"exact> <div> As ssSupport page</div> </Route>
        </Switch>
        </>
    );

    
}






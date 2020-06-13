import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import Home from "./home/home.jsx";


import Authentication from "_services/auth_service.js";


import 'css/app.css';

class App extends React.Component{
    constructor(props){
        super(props);
        Authentication.login('maciek', 'lody10');


        this.state = {
            user: Authentication.get_user(),
            header: 999,
        }
        
        Authentication.add_subscriber((user)=>
            this.setState({user: user})
        );

    }

    render(){

        return (
            <Router>
                <Route>
                    <Home user={this.state.user}/>
                
                
                </Route>
            </Router>
        )
    }
}


ReactDOM.render(
    <App/>,
    document.getElementById("root")
);
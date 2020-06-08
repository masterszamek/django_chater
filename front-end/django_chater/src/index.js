import React from 'react';
import ReactDOM from 'react-dom';
import Authentication from "./_services/auth_service.js";
// import {get_auth_header} from "./_helpers/auth_header.js";


class App extends React.Component{
    constructor(props){
        super(props);
        Authentication.login('maciek', 'lody10');


        this.state = {
            user: Authentication.get_user_info(),
            header: 999,
        }
        
        Authentication.add_subscriber((user)=>
            this.setState({user: user})
        );
        window.setInterval(async (param1)=>{
                const sroken = await Authentication.get_auth_header();
                console.log(sroken, param1);
                param1.setState({header: sroken});
            },
            1000*30,
            this,

        );
    }
    async componentDidMount(){
        const headerr = await Authentication.get_auth_header();
        this.setState({header:headerr});
    }
    render(){
        
        return (<div>
            <div> {this.state.user.authenticated ? "Autoryzowany" : "Nie Autoryzowany"}</div>
            <div> {this.state.header.Authorization}</div>
            </div>
        )
    }
}


ReactDOM.render(
    <App/>,
    document.getElementById("root")
);
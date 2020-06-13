import {config} from "../config.js";
import {perform_request_or_401} from "./../_helpers/perform_request.js";


export default class Authentication{
    static #user = {
        authenticated: false,
    };

    static #access_token = {
        token: undefined,
        expiry: undefined,
    }
    static #subscribers = [];


    static async login(username, password){
        const user_form = {
            "username": username,
            "password": password, 
        };
        const datee1 = new Date().getTime();
        const response = await fetch(config.api_url+"api/token/",
            {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": JSON.stringify(user_form),
            }
        );
        const datee2 = new Date().getTime();
        console.log(datee2-datee1);
        console.log(response);
        if(response.ok){
            this.set_user_authenticated(true);
            const data = await response.json();

            this.set_refresh_token(data.refresh);
            this.set_access_token(data.access);    
        }
        else
            this.set_user_authenticated(false);

    };
    static logout(){
        this.set_user_authenticated(false);
        this.set_access_token(undefined);
        localStorage.removeItem("refresh_token");

    }
    
    static get_user(){
        return this.#user;
    }

    static set_user_authenticated(authenticated){
        this.#user.authenticated = authenticated;

        this.#subscribers.forEach((func)=>{
            func(this.get_user());
        })
    }
    
    static async get_auth_header(){
        
        const access_token = await this.get_access_token();
  
        return {Authorization: `Bearer ${access_token}`};
    }
    
    static set_access_token(token){
        let expiry;
        if(token === undefined)
            expiry = 0;
        else
            expiry = new Date( new Date().getTime() + config.access_token_lifetime*1000) ;

        this.#access_token.token = token;
        this.#access_token.expiry = expiry;
    };

    static set_refresh_token(token){
        localStorage.setItem("refresh_token", token);
    };

   
    
    static async get_access_token(){
        const current_time = new Date().getTime();

        if(this.#access_token.expiry > current_time)
            return this.#access_token.token;

        const form_data = {
            "refresh": localStorage.getItem("refresh_token")
        };
    
        const response = await perform_request_or_401(
            config.api_url+"api/token/refresh/",
            {
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": JSON.stringify(form_data)
            }    
        );
        console.log(response);
        if(response.ok){
            const data = await response.json();
            this.set_user_authenticated(true);
            this.set_access_token(data.access);
            console.error("zapytanie ok");

            return data.access;
        }
        else{
            this.set_access_token(undefined);
            this.set_user_authenticated(false);
            console.error("401");
            return undefined;
        }
    };

    static add_subscriber(func){
        this.#subscribers.push(func);
    }

}















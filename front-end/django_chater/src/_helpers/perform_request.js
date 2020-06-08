import Authenticate from "../_services/auth_service.js";


export async function perform_request_or_401(url, data){
    let response = await fetch(url, data);
    if(!response.ok && response.status==401){
        Authenticate.set_user_authenticated(false);
    }

    return response;

}
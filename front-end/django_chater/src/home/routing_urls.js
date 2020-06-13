import include_urls from '_helpers/include_urls';

const root_url = "/";


const support_urls = {
    about_me: 'about_me/',
    contact: 'contact/',
    ideas: 'ideas/',
}
const settings_urls = {
    change_password: "change_password",
}

const urls = include_urls(root_url, {
    home: '',
    sign_in: 'sign_in/',
    sign_up: 'sign_up/',
    workspaces: 'workspaces/',
    support: include_urls('support/', support_urls),
    settings: include_urls("settings/", settings_urls),

})

export {urls as default}
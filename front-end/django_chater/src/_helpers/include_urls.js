function include_urls(path, urls){
    let new_obj = {};
    for(let key in urls){
        if(typeof(urls[key]) === "object"){
            new_obj[key] = include_urls(path, urls[key])
        }
        else
            new_obj[key] = `${path}${urls[key]}`;
    
    }
    return new_obj;
}

export {include_urls as default}
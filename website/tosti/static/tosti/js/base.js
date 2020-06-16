
let update_timer = null;
let update_list = [];

function create_element(tag_name, class_list, text) {
    let element = document.createElement(tag_name);
    for (let i = 0; i < class_list.length; i++) {
        element.classList.add(class_list[i]);
    }
    element.appendChild(document.createTextNode(text));
    return element;
}

function set_cookie(name,value,days) {
    let expires = "";
    value = encodeURI(value);
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function get_cookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for(let i=0;i < ca.length;i++) {
        let c = ca[i];
        while (c.charAt(0)===' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) === 0) return decodeURI(c.substring(nameEQ.length,c.length));
    }
    return null;
}

function erase_cookie(name) {
    document.cookie = name+'=; path=/; domain=kanikervanaf.nl; Max-Age=-99999999;';
}

function set_list_cookie(name, list, days) {
	try {
		let string = JSON.stringify(list);
		set_cookie(name, string, days);
	    return true;
	}
	catch(error) {
        return false;
    }
}

function update_and_replace(data_url, container, data) {
    let csrf_token = get_cookie('csrftoken');
    jQuery(function($) {
        data.csrfmiddlewaretoken = csrf_token;
        $.ajax({type: 'POST', url: data_url, data, dataType:'json', asynch: true, success:
            function(data) {
                replace_container(container, data.data)
            }}).fail(function() {
                console.error("Failed to update " + container);
            });
        }
    )
}

function update_and_callback(data_url, data, callback/*, args */) {
    let args = Array.prototype.slice.call(arguments, 3);
    let csrf_token = get_cookie('csrftoken');
    jQuery(function($) {
        data.csrfmiddlewaretoken = csrf_token;
        $.ajax({type: 'POST', url: data_url, data, dataType:'json', asynch: true, success:
            function(data) {
                args.unshift(data);
                callback.apply(this, args);
            }}).fail(function() {
                console.error("Failed to update " + container);
            });
        }
    )
}

function replace_container(container, data) {
    container.innerHTML = data;
}

function add_update_list(func, args) {
    update_list.push({func: func, args: args});
}

function update_update_list() {
    clearTimeout(update_timer);
    for (let i = 0; i < update_list.length; i++) {
        update_list[i].func.apply(this, update_list[i].args);
    }
    update_timer = setTimeout(update_update_list, 5000);
}

$(document).ready(function() {
    update_update_list();
});
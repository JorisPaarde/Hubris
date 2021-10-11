$( document ).ready(function() {

var action = ""
var enemy = "notspecified"

// https://docs.djangoproject.com/en/3.2/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
// https://docs.djangoproject.com/en/3.2/ref/csrf/

$( ".action-icon-button" ).click(function() {
    // get the first classname this is also the action name.
    let classes = $(this).find(".action-icon").attr("class");
    action = classes.substr(0,classes.indexOf(' '));
    // if the action does't need a target specified, send the data
    if ((action == "healing") || (action == "ice") || (action == "skip") ){
        data = {
            'enemy': enemy,
            'action':action,
        };

        fetch(URL, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
                body: JSON.stringify({'post_data':data}) //JavaScript object of data to POST
                })
            .then(response => {
                return response
            });
    }
    else{
        // enemys get enemy select class to indicate they can be attacked
        $(".enemy-image").addClass("enemy-select");
    };
   
    });

$( ".enemy-image" ).click(function() {

    if ($(this).hasClass('enemy-select')) {
        // when this enemy is clicked
        let classes = $(this).closest(".game-floor-enemy").attr("class");
        enemy = classes.substr(0,classes.indexOf(' '));
        // send correct action and enemy id value to action processor view
        data = {
            'enemy': enemy,
            'action':action,
        };

        fetch(URL, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken,
            },
                body: JSON.stringify({'post_data':data}) //JavaScript object of data to POST
                })
            .then(response => {
                return response
            });
        };
    });
});

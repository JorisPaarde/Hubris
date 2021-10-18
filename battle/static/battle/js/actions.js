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
            };
        };
    };
    return cookieValue;
};

const csrftoken = getCookie('csrftoken');
// https://docs.djangoproject.com/en/3.2/ref/csrf/


$( ".action-icon-button" ).click(function() {
    // get the first classname this is also the action name.
    let classes = $(this).find(".action-icon").attr("class");
    action = classes.substr(0,classes.indexOf(' '));

    // if the icon is muted it can not be used
    isMuted = classes.includes("text-muted")
    if (isMuted){
        return
    };

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
                setTimeout(location.reload(), 2000)
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
                location.reload()
                return response
            });
        };
    });

function checkEnemyHealth() {
    let gameStepNr = parseInt($(" .game-step-nr ").data("step"))
    var totalHealth = 0
    if ($( ".game-floor-enemy" ).length > 0){
        // adds up all enemies health
        $( ".enemy-health-current" ).each(function () {
            totalHealth = totalHealth + parseInt($(this).html())
            });
        // if the total is 0 confirmation is send to the backend that they are all dead
        console.log(totalHealth)
        if ((totalHealth == 0)&&(gameStepNr == 2)){
        confirmAllDead();
        };
    };  
};

checkEnemyHealth();

function confirmAllDead() {
    data = {
        'all_enemies_dead': true,
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
            setTimeout(window.location.replace(response.url), 2000)
            return response
        }); 
    };
});

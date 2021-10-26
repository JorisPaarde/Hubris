$(document).ready(function () {

    var action = ""
    var enemy = "notspecified"

    // function to get the csrf token
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

    // function to handle action bar clicks
    $(".action-icon-button").click(function () {
        // get the first classname this is also the action name.
        let classes = $(this).find(".action-icon").attr("class");
        action = classes.substr(0, classes.indexOf(' '));

        // if the icon is muted it can not be used
        isMuted = classes.includes("text-muted")
        if (isMuted) {
            return
        };

        // if the action does't need a target specified, send the data
        if ((action == "healing") || (action == "ice") || (action == "skip")) {
            data = {
                'enemy': enemy,
                'action': action,
            };

            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'post_data': data
                    }) //JavaScript object of data to POST
                })
                .then(response => {
                    $("#message-text").html(`you chose ${action}`);
                    toggleMessage();
                    setTimeout(reload, 1000)
                    return response
                });
        } else {
            // enemys get enemy select class to indicate they can be attacked
            $("#message-text").html(`select an enemy to attack with ${action}`);
            toggleMessage();
            setTimeout(toggleMessage, 1000);
            $(".enemy-image").addClass("enemy-select");
        };
    });

    // funtion to handle enemy attack selection clicks
    $(".enemy-image").click(function () {

        if ($(this).hasClass('enemy-select')) {
            // when this enemy is clicked
            let classes = $(this).closest(".game-floor-enemy").attr("class");
            enemy = classes.substr(0, classes.indexOf(' '));
            // send correct action and enemy id value to action processor view
            data = {
                'enemy': enemy,
                'action': action,
            };

            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'post_data': data
                    }) //JavaScript object of data to POST
                })
                .then(response => {
                    reload()
                    return response
                });
        };
    });

    // function to check if enemy's are dead
    function checkEnemyHealth() {
        console.log('checking health')
        let gameStepNr = parseInt($(" .game-step-nr ").data("step"));
        let totalHealth = 0;
        if ($(".game-floor-enemy").length >= 0) {
            // adds up all enemies health
            $(".enemy-health-current").each(function () {
                totalHealth = totalHealth + parseInt($(this).html())
            });
            // if the total is 0 confirmation is send to the backend that they are all dead
            if ((totalHealth == 0) && (gameStepNr == 2)) {
                message = `U killed all enemies!!`
                $("#message-text").html(message);
                toggleMessage();
                setTimeout(confirmAllDead, 2000);
            };
        };
    };

    checkEnemyHealth();

    // function to confirm to the backend that all enemies died
    function confirmAllDead() {
        data = {
            'all_enemies_dead': true,
        };

        fetch(URL, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'post_data': data
                }) //JavaScript object of data to POST
            })
            .then(response => {
                window.location.replace(response.url)
                return response
            });
    };

    // function to check if enemies are attacking
    function checkEnemyAttack() {
        let gameStepNr = parseInt($(" .game-step-nr ").data("step"));
        let currentPhase = $(" .game-phase-nr ").data("phase");
        if (($(".game-floor-enemy").length > 0)&&(gameStepNr == 2)){
            $(".game-floor-enemy").each(function () {
                let enemy = $(this)
                let enemyName = $(this).data("enemy");
                let enemyClass = $(this).attr("class");
                let enemyId = enemyClass.substr(0, enemyClass.indexOf(' '));
                let enemyAttackPhase = $(this).find(" .enemy-attack-phase-icon ").html().toLowerCase();
                let enemyHealth = parseInt($(this).find(" .enemy-health-current ").html());
                // detect wether this enemy has already attacked
                let hasNotAttacked =  enemy.hasClass('False');
                if ((enemyAttackPhase == currentPhase)&&(enemyHealth > 0)&&(hasNotAttacked)){
                    // send correct action and enemy id value to enemy action processor view
                    data = {
                        'enemy': enemyId,
                        'enemy_action': 'attacks',
                    };

                    fetch(URL, {
                            method: 'POST',
                            credentials: 'same-origin',
                            headers: {
                                'Accept': 'application/json',
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': csrftoken,
                            },
                            body: JSON.stringify({
                                'post_data': data
                            }) //JavaScript object of data to POST
                        })
                        .then(response => {
                            // player gets indication of enemy that attacked
                            $("#message-text").html(`u where attacked by ${enemyName}!`);
                            toggleMessage();
                            setTimeout(reload, 2000);
                            return response
                        });
                };
            });
        };
    };
    checkEnemyAttack();
});

// helper functions

function reload() {
    location.reload()
}

function toggleMessage() {
    $(".message-screen").toggleClass("d-none");
}
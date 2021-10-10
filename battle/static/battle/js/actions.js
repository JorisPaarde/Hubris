$( document ).ready(function() {

var action = ""
var enemy = ""

$( ".action-icon-button" ).click(function() {
    // get the first classname this is also the action name.
    let classes = $(this).find(".action-icon").attr("class");
    action = classes.substr(0,classes.indexOf(' '));
    console.log(action);
    });

$( ".enemy-select" ).click(function() {
    // when this enemy is clicked
    let classes = $(this).closest(".game-floor-enemy").attr("class");
    enemy = classes.substr(0,classes.indexOf(' '));
    // add form html to enemies with correct action and enemy id value
    html = `
        <form class="enemy-form d-none"
            action="{% url 'battle:action_processor' '${enemy} ${action}' %}" method="POST">
            {% csrf_token %}
            <button class="action-icon-button enemy-select-button" type="submit"></button>
        </form>
        `
    $(this).before(html);
    });

});

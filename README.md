# Strategy plane:

Creating an entertaining gaming experience.
Replayable game.
Competitive game.
Appealing graphics.
Requires some skill.
Collectables / joy of finding new stuff.
Partially free to entice users.
Able to play any time casually and continue if u want.
Easy to understand rules

Scope:
navigation menu
login/registration
payment section
how to play
wiki
continue last game/ start new one
block portrait mode in game

game:
magic spells
health
defence
different enemies with different stats
experience?
Leaderboard
select your hero
coninue last game

not: weapons, shields, rings etc.

# Structure:

main menu with:
register > login > play free/paid
login > play free/paid
full version buy > checkout > play now
wiki >home / play
leaderboard > main menu
how to play
play now free > full version buy > checkout

game:
start of game > select player > card selection  > play phase 1-5 > next level? > get cards and discard 

# Skeleton:

figma design

# Surface:

fonts
color sceme
artwork

# User stories:

– As a site owner, i want to:
    1. Offer a replayable game. That users enjoy playing again and again.(game should be different every time ea. Random selection of enemies and cards. Aslo different starting hero)
    2. Entice people to buy the full version.(clear explanation of what u get and easy access to the checkout. Also the free version as a teaser.)
    3. Make it as easy as possible (minimize #actions) for users to register and login. (username/password or google account.)
    4. Make it as easy as possible (minimize #actions) to pay for the full version. (apple / google pay / creditcard)
    5. Add / edit / delete cards, starting player stats, and enemies in the database.
    6. Have a secured access to the admin.(provided by oath)

– As a first time user, i want to:
    1. Login / register with username/password or google account.
    2. Reset my password.
    3. Learn the game rules.
    4. Learn the UI.
    5. See what monsters and spells are in the game through a wiki page.
    6. Try the free version to see if i like the game.
    7. Find out what i get in the full version. (also after i play the free game)
    8. See an indication that i’m on the free version.
    9. Pay for the full version with the least amount of effort.

– As a paying user, i want to:
    1. Play the game now. (minimize #actions after login: play now? / menu)
    2. Contact the site owner.
    3. See what monsters and spells are in the game.
    4. Access the leaderboard.
    5. Continue my game or start a new one.
    6. Have a replayable game. That i enjoy playing again and again.

– As a player who plays the game, i want to:
    1. play in fullscreen
    2. Select a wizard to play with.
    3. See all the properties of the different wizards.
    4. Have a clear overview of the cards in my hand.
    5. See all spell information on the cards: title, description, phase, style, effects and cost.
    6. Select  a card from my deck to play.
    7. Discard a card from my hand.
    8. Decide if i want to go up a level.
    9. See an indication of the level i’m at.
    10. See an indication of the battle phase i’m in.
    11. See all my stats in the stats bar.
    12. See the stats of my enemies.
    13. See my score.
    14. See the spell effects and cost in the spell selection bar
    15. Select a spell available to me in this phase.
    16. Select which enemy to attack.
    17. Skip to the next phase.
    18. Know when i get an extra card for my xp.

– As a player who plays the game on mobile, i want to:
    1. Have a fullscreen gaming experience
    2. Play the game in landscape mode only so i get the best experience.

– As a user who uses the wiki page, i want to:
    1. search cards by type, level, phase, effect(heal/attack/drain/defence)
    2. sort cards by cost
    3. search enemies by type, xp, phase
    4. sort enemies by attack power, health

# Bugs:

Google login resulted in : "Error 400: redirect_uri_mismatch"
Menu button was not clickable in game screen. Fixed by making sure no div was blocking it with a higher z-index value.
Player selection layout broke on wider screens. pushed text to the bottom of the container.
hand-cards where added but not associated with player hand. Changed model to many to many field and corrected card draw function.
When comparing players hand card to the cards in the database the values seemed the same, but did not trigger an if equal statement.
Back button press after playing a card made it possible to play infinite cards. Added a check for the gamestep to be '2' to prevent this.
Restarting the game resulted in an ever increasing list of hand cards. Deleting them when restarting a game.
Restarting a game resulted in no enemies shown. Deleting the old ones in the database fixed this.
Possibility to have 2 open games resulted in errors. created try except logic to complete the oldest game.
Player having completed games resulted in MultipleObjectsReturned. Added check in all views to get the game that is not finished.
After deployment, pickmonsters function trew an error on the length of skillstyle and attackphase values, changed input from value ('LN') to key ('Lightning').
The player death view did not run but, gave a 200 status code... Moving it to another app fixed this. why? no idea...
Attacking a player resuted in errors, updated check for enemy to: "hasattr(target, 'enemy')" instead of "target.enemy".
When dieing, player needed to discard multiple cards and draw new ones to get to 8 cards again. Now draws cards function draws new cards to fill hand to 8.
After player death, gamefloor enemy's where not deleted, causing the database to fill with unused enemys. Added deleting all enemys to the player death function.

# technologies used:

https://ezgif.com/maker


# Code

models profile
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
settings
https://github.com/Code-Institute-Solutions/boutique_ado_v1/blob/a07c1ca5a3b973eb47e5c944829cea06ead3936d/boutique_ado/settings.py



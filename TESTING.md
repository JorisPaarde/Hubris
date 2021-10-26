# Tests and bugreports:

- [User story testing](#user-story-testing)
- [Responsive layout testing](#responsive-visual-layout-testing)
- [Feature testing](#feature-testing)
- [Browser testing](#browser-testing)
- [Validators](#validators)
- [Lighthouse Report](#lighthouse-report)
- [Bugs during development](#bugs-encountered-during-development-and-their-fixes)

# User story testing:

## General functionality:

<br>
<br>

### As a Site owner, I want to:
---
user story|implementation
----|----
Offer a replayable game. That users enjoy playing again and again.(game should be different every time ea. Random selection of enemies and cards. Also different starting hero)|
Entice people to buy the full version.(clear explanation of what u get and easy access to the checkout. Also the free version as a teaser.)|...
Make it as easy as possible (minimize #actions) for users to register and login. (username/password)|...
Make it as easy as possible (minimize #actions) to pay for the full version. (google pay / creditcard)|...
Add / edit / delete cards, starting player stats, and enemies in the database.|...
Have a secured access to the admin.(provided by oath)|...

<br>
<br>

### As a first time user, I want to:
---
user story|implementation
----|----
Login / register with username/password.|...
Reset my password.|...
Learn the game rules.|...
Learn the UI of the game.|...
See what monsters and spells are in the game through a wiki page.|...
Try the free version to see if i like the game.|...
Find out what i get in the full version. (also after i play the free game)|...
See an indication that i’m on the free version.|...
Pay for the full version with the least amount of effort.|...

<br>
<br>

### As a paying user, I want to:
---
user story|implementation
----|----
Play the game now. (minimize #actions after login: play now? / menu)|...
See what monsters and spells are in the game.|...
Access the leaderboard.|...
Continue my game or start a new one.|...
Have a replayable game. That i enjoy playing again and again.|...

<br>
<br>

### As a player who plays the game, i want to:
---
user story|implementation
----|----
Play in fullscreen.|...
Select a wizard to play with.|...
See all the properties of the different wizards.|...
Have a clear overview of the cards in my hand.|...
See all spell information on the cards: title, description, phase, style, effects and cost.|...
Select  a card from my deck to play.|...
Discard a card from my hand.|...
Decide if i want to go up a level.|...
See an indication of the level i’m at.|...
See an indication of the battle phase i’m in.|...
See all my stats in the stats bar.|...
See the stats of my enemies.|...
See my score.|...
See the spell effects and cost in the spell selection bar.|...
Select a spell available to me in this phase.|...
Select which enemy to attack.|...
Skip to the next phase.|...

<br>
<br>

### As a player who plays the game on mobile, i want to:
---
user story|implementation
----|----
Have a fullscreen gaming experience
Play the game in landscape mode only so i get the best experience.

<br>
<br>

### As a user who uses the wiki page, i want to:
---
user story|implementation
----|----
Search cards by type, free version availability or attack-phase.|...
Sort cards by cost.|...

<br>
<br>

# Responsive visual layout testing

## main page

feature|expected behaviour|testing|result|Fix(if needed)
---|---|---|---|---


<br>
<br>

# Feature testing

## Form validation

feature|expected behaviour|testing|result|Fix(if needed)
---|---|---|---|---

<br>

## Other features

feature|expected behaviour|testing|result|Fix(if needed)
---|---|---|---|---


<br>

# Browser testing

Browser|layout correct|functionality correct|Issues
---|---|---|---
Opera|Yes|Yes|None
Chrome|Yes|Yes|None
Edge|Yes|Yes|None
Firefox|Yes|Yes|None

<br>

# Validators

## To validate the html and CSS [W3C markup validation](https://validator.w3.org/) was used.

### index.html:
### battle.html:
### player-select.html:
### proceed-to-next-floor.html:
### register.html:
### login.html:
### leaderboard.html:
### how-to-play.html:
### wiki.html:

<br>

For the CSS the results were as follows:

### base.css
### battle.css
### full-version.css
### profiles.css
### wiki.css

<br>

## For Javascript validation [JSHint](https://jshint.com/) was used.

### actions.js
### checkout.js
### force_landscape.js

<br>

## For python validation [pep8online](http://pep8online.com/) was used.

### battle: utils.py
### battle.views.py
### battle.models.py
### battle.admin.py
### battle.urls.py

### checkout.urls.py
### checkout.views.py

### profiles.views.py
### profiles.utils.py
### profiles.models.py
### profiles.urls.py

### wiki.forms.py
### wiki.urls.py
### wiki.views.py

<br>

# Lighthouse Report 

## desktop
### index.html:
### battle.html:
### player-select.html:
### proceed-to-next-floor.html:
### register.html:
### login.html:
### leaderboard.html:
### how-to-play.html:
### wiki.html:

## mobile
### index.html:
### battle.html:
### player-select.html:
### proceed-to-next-floor.html:
### register.html:
### login.html:
### leaderboard.html:
### how-to-play.html:
### wiki.html:
<br>

# Bugs encountered during development and their fixes:

bug|fix
---|---
Menu button was not clickable in game screen. |Fixed by making sure no div was blocking it with a higher z-index value.
Player selection layout broke on wider screens. |Pushed text to the bottom of the container.
hand-cards where added but not associated with player hand. |Changed model to many to many field and corrected card draw function.
When comparing players hand card to the cards in the database the values seemed the same, but did not trigger an if equal statement. |Fixed by adding a lower statement to both values.
Back button press after playing a card made it possible to play infinite cards. |Added a check for the gamestep to be '2' to prevent this.
Restarting the game resulted in an ever increasing list of hand cards. |Deleting them when restarting a game.
Restarting a game resulted in no enemies shown. |Deleting the old ones in the database fixed this.
Possibility to have 2 open games resulted in errors. |Created try except logic to complete the oldest game.
Player having completed games resulted in MultipleObjectsReturned. |Added check in all views to get the game that is not finished.
After deployment, pickmonsters function trew an error on the length of skillstyle and attackphase values. |Changed input from value ('LN') to key ('Lightning').
The player death view did not run but, gave a 200 status code... |Moving it to another app fixed this. why? no idea...
Attacking a player resuted in errors. |updated check for enemy to: "hasattr(target, 'enemy')" instead of "target.enemy".
When dieing, player needed to discard multiple cards and draw new ones to get to 8 cards again. |Now draws cards function draws new cards to fill hand to 8.
After player death, gamefloor enemy's where not deleted, causing the database to fill with unused enemys. |Added deleting all enemys to the player death function.
When starting a new game, all scores where deleted from a player, because the player was deleted. |Fixed by resetting stats rather than deleting player.
Enemies had mana or heal skill selected, resulting in attack icon errors. |Added separate enemy attackstyle list to settings.
When killing enemys or being attacked, the order of the enemy's changed in the template due to the data not being deterministic. |Added a meta base class to order the data by pk.


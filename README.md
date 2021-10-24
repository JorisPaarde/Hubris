# Hubris

## The magic card batle game

some short description

[View the live project here](https://hubris-the-game.herokuapp.com/)

![Hubris mockup image]()

# Table of Contents

- [UX](#user-experience-(ux))
  - [User stories](#user-stories)
  - [Design](#design)
  - [Mockup](#mockup)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment-and-cloning)
- [Credits](#credits)

# User experience (ux)

## User stories:

- As a site owner, i want to:
    1. Offer a replayable game. That users enjoy playing again and again.(game should be different every time ea. Random selection of enemies and cards. Aslo different starting hero)
    2. Entice people to buy the full version.(clear explanation of what u get and easy access to the checkout. Also the free version as a teaser.)
    3. Make it as easy as possible (minimize #actions) for users to register and login. (username/password or google account.)
    4. Make it as easy as possible (minimize #actions) to pay for the full version. (apple / google pay / creditcard)
    5. Add / edit / delete cards, starting player stats, and enemies in the database.
    6. Have a secured access to the admin.(provided by oath)

- As a first time user, i want to:
    1. Login / register with username/password or google account.
    2. Reset my password.
    3. Learn the game rules.
    4. Learn the UI.
    5. See what monsters and spells are in the game through a wiki page.
    6. Try the free version to see if i like the game.
    7. Find out what i get in the full version. (also after i play the free game)
    8. See an indication that i’m on the free version.
    9. Pay for the full version with the least amount of effort.

- As a paying user, i want to:
    1. Play the game now. (minimize #actions after login: play now? / menu)
    2. Contact the site owner.
    3. See what monsters and spells are in the game.
    4. Access the leaderboard.
    5. Continue my game or start a new one.
    6. Have a replayable game. That i enjoy playing again and again.

- As a player who plays the game, i want to:
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

- As a player who plays the game on mobile, i want to:
    1. Have a fullscreen gaming experience
    2. Play the game in landscape mode only so i get the best experience.

- As a user who uses the wiki page, i want to:
    1. search cards by type, level, phase, effect(heal/attack/drain/defence)
    2. sort cards by cost
    3. search enemies by type, xp, phase
    4. sort enemies by attack power, health


### First time user:

As a first time user i want to:

- 

### Recurring user:

- 

# Design


## Colour Scheme


### Fonts


## Database schema

### Original database design:

This original desing was made in dbdiagram, and can be acessed via this [link]()
![Schema](readme-images/db-schema.png)

During development turned out ....

### Database models in django:

## Imagery

The following images where used:

## Mockup

-  The mockup design of this site was made in Figma. U can view it [here](https://www.figma.com/file/p55Dty6wFf4cGkjfJhYHT4/Hubris-1.0?node-id=0%3A1) 

![Hubris mockup image](readme-images/design-mockup.jpg)

# Features

- 

## future features

- 

# technologies used:

https://ezgif.com/maker


### Languages Used

-   [HTML5](https://en.wikipedia.org/wiki/HTML5)
    - HTML5 was used to build the main structure and content of the page.
-   [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
    - CSS3 was used to give the html styling and layout.
    And to make the page responsive to differentscreen sizes.
-   [Javascript](https://nl.wikipedia.org/wiki/JavaScript)
    - Javascript was used for
-   [Python](https://www.python.org/)
    - Python was used for writing 
-   [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
    - Jinja was used for writing the template code.


### Frameworks, Libraries & Programs Used

1. [Materialize css 0.100.2:](http://archives.materializecss.com/0.100.2/getting-started.html)
    - Materialize was used to create the responsive structure of the website.
1. [jQuery:](https://jquery.com/)
    - jQuery Used among other things in script file to initialze materialize scripts.
1. [Git](https://git-scm.com/)
    - Git was used for version control by utilizing the terminal in gitpod to regularly commit, with comments, to Git and Push to GitHub.
1. [GitHub:](https://github.com/)
    - GitHub is used to store the projects code and assets and to fork the project for the customer.
1. [Figma:](https://figma.com/)
    - Figma was used to create the website design and prototype.
1. [Heroku:](https://www.heroku.com)
    - Heroku was used to deploy the app.
1. [dbdiagram](https://dbdiagram.io/)
    - To design the database schema.

# Testing

All testing can be found [here](TESTING.md).

## Bugs:

- Google login resulted in : "Error 400: redirect_uri_mismatch"
- Menu button was not clickable in game screen. Fixed by making sure no div was blocking it with a higher z-index value.
- Player selection layout broke on wider screens. pushed text to the bottom of the container.
- hand-cards where added but not associated with player hand. Changed model to many to many field and corrected card draw function.
- When comparing players hand card to the cards in the database the values seemed the same, but did not trigger an if equal statement.
- Back button press after playing a card made it possible to play infinite cards. Added a check for the gamestep to be '2' to prevent this.
- Restarting the game resulted in an ever increasing list of hand cards. Deleting them when restarting a game.
- Restarting a game resulted in no enemies shown. Deleting the old ones in the database fixed this.
- Possibility to have 2 open games resulted in errors. created try except logic to complete the oldest game.
- Player having completed games resulted in MultipleObjectsReturned. Added check in all views to get the game that is not finished.
- After deployment, pickmonsters function trew an error on the length of skillstyle and attackphase values, changed input from value ('LN') to key ('Lightning').
- The player death view did not run but, gave a 200 status code... Moving it to another app fixed this. why? no idea...
- Attacking a player resuted in errors, updated check for enemy to: "hasattr(target, 'enemy')" instead of "target.enemy".
- When dieing, player needed to discard multiple cards and draw new ones to get to 8 cards again. Now draws cards function draws new cards to fill hand to 8.
- After player death, gamefloor enemy's where not deleted, causing the database to fill with unused enemys. Added deleting all enemys to the player death function.
- When starting a new game, all scores where deleted from a player, because the player was deleted. fixed by resetting stats rather than deleting player.
- Enemies had mana or heal skill selected, resulting in attack icon errors. Added separate enemy attackstyle list to settings.


# Deployment and cloning

### Clone this repository:
### In linux:
To find the link, go to the "code" dropdown menu in this repository.
Click the clipboard icon next to the url.
In your terminal type:

```
$mkdir <jour project directory>
$git init <jour project directory> (to set up a new repository)
$git clone https://github.com/JorisPaarde/my-vegan-recipes.git
```

In Windows:

follow [these](https://www.jcchouinard.com/clone-github-repository-on-windows/) steps.

Install all requirements through the requirements.txt file:
```
pip install -r requirements.txt
```

### Create your account 

## To deploy this project on Heroku: 

- Create your account on Heroku here: https://signup.heroku.com/login

- Create a new app on heroku:

- Go to: https://dashboard.heroku.com/apps
select new, create new app from the dropdown menu on the right.
Enter your app-name and region and click create app.
Under delpoyment method, select github.

![github connect](readme-images/github-connect.png)

- Select your repository and connect.

- Go to settings, config vars and enter the variables for

![Config vars](readme-images/Inkedheroku_vars.jpg)

- Go to deploy and at the bottom of the page manually deploy your main github branch

Your app is now deployed and ready to run.
At the top of th epage click open app to run it.

# Credits


Thanks to Precious for his mentoring.
And of course all the people on slack.


## Code

The following code was copied from external sources:


- models profile
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
- settings
https://github.com/Code-Institute-Solutions/boutique_ado_v1/blob/a07c1ca5a3b973eb47e5c944829cea06ead3936d/boutique_ado/settings.py
- stripe
https://testdriven.io/blog/django-stripe-tutorial/

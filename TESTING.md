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
- When killing enemys or being attacked, the order of the enemy's changed in the template due to the data not being deterministic. Added a meta base class to order the data by pk.


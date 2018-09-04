# synapsBot
This is just a personal bot for my server. I hope you can figure out what my code does. Feel welcome to contact me on Discord @Mehvix#7172 


If you keep getting an error code when trying to write to the `users.json` file it's probably because you have multiple versions of the same bot running at the same time.


## Cogs / Files 

### [.default_formatting.py](https://github.com/Mehvix/synapsBot/blob/master/.default_formatting.py)

Template for when I make a new cog.


### [admin.py](https://github.com/Mehvix/synapsBot/blob/master/admin.py)

Admin-exclusive commands.


### [basic.py](https://github.com/Mehvix/synapsBot/blob/master/basic.py)

Very simple commands everyone in the server can use.


### [createpoll.py](https://github.com/Mehvix/synapsBot/blob/master/createpoll.py)

Cog for the .createpoll command. Moved out of `verified.py` because it took up too much space.


### [curtime.py](https://github.com/Mehvix/synapsBot/blob/master/curtime.py)

Used to track uptime and cur(rent) time.


### [forwarding.py](https://github.com/Mehvix/synapsBot/blob/master/forwarding.py)

Forwards all DM's the bot sends and recieves to the owner (me.)


### [insults.json](https://github.com/Mehvix/synapsBot/blob/master/insults.json)

All insults for .insult command (in `verified.py`)
Found this from [TwentySixe's Github.](https://github.com/Twentysix26/26-Cogs/blob/master/insult/data/insults.json)


### [karma.py](https://github.com/Mehvix/synapsBot/blob/master/karma.py)

For managing levels and karma (users.json)


### [music.py](https://github.com/Mehvix/synapsBot/blob/master/music.py)

Simple music bot. Used for when Rythm is down.


### [notifications.py](https://github.com/Mehvix/synapsBot/blob/master/notifications.py)

Messages for when people join/leave/.accept/are banned from sever.


### [roulette_outcomes](https://github.com/Mehvix/synapsBot/blob/master/roulette_outcomes.json) / [users.json](https://github.com/Mehvix/synapsBot/blob/master/users.json)

Backups for if anything goes wrong.


### [settings.py](https://github.com/Mehvix/synapsBot/blob/master/settings.py)

Where server settings are stored for my main server and my testing server.

### [synapsBot_X.XX(2.20)](https://github.com/Mehvix/synapsBot/blob/master/synapsBot_2.20.py)

Host file. Holds a few commands, such as `.ping`  but not much else.

### [verified.py](https://github.com/Mehvix/synapsBot/blob/master/verified.py)

Verified-exclusive commands (cool-kid stuff.)

### [zalgo.py](https://github.com/Mehvix/synapsBot/blob/master/zalgo.py)

For generating z͗̎͟aͫͯ́l͍̩̔ġ͘͞o͌ͬ̏҉̴̡̧ text with zalgo command in .verified

### [typeracer.py](https://github.com/Mehvix/synapsBot/blob/master/typeracer.py)

Gets stats for a user's typeracer.com account

### [canvas.py](https://github.com/Mehvix/synapsBot/blob/master/canvas.py)

It's like [reddit.com/r/place](https://www.reddit.com/r/place/) but for discord and a lot smaller

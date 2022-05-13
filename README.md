# Ratatouiile
Discord bot - Tema la taille du rat

### Requirements
Requires the ```discord.py``` api.

### wtf is that
Makes random sentences about 'tema la taille du rat',
basing itself on 3 lists stored in the ```data.json``` file.

### How to use
1. Create a new bot using the discord dev portal, and copy token.
2. Paste token in the ```token``` file.
3. Invite the bot on your server and launch the ```main.py``` script.

The bot is now running. Every time an user in a channel includes 'rat'
in a message, the bot will respond with a randomly generated sentence.

Users can add words to the ```data.json``` list to make it bigger.
They can use the ```!add <position> <word>``` command, where position
is the position of the word in the sentence (for instance: 'tema' is 1,
'la taille' is 2, and 'du rat' is 3), followed with the word they want
to add.
The words are not written yet, they need to be accepted by a mod that as
the role ```ratatouilleur```. This role can be changed by modifying the
value at the top of the script. Mods manage waiting words using the
```!check``` command, which will return each submitted word allong with
an id, and choose either to delete it using ```!make rm <id>``` or to
accept it using ```!make ok <id>```.

Note 1: the ids change each time an element is deleted or accepted, ik
this is bad but idc

Note 2: Users have to precise the article while submiting a word.
For instance, dont submit 'muridé' but 'du muridé'.

Have a great day

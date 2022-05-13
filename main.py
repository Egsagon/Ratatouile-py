# =================== #
# = Ratatouille bot = #
# =================== #

import json
import discord
from random import randint
from os.path import exists

# Create data.json if nescessary
if not exists('data.json'):
    f = open('data.json', 'w+')
    f.write('[]')
    f.close()


# Settings
triggers = ['ratatouille', 'tema', 'taille', 'rat', '🐀', ':rat:']
modRole = 'ratatouilleur'

def pick() -> tuple:
    """Pick 3 values in each DATA list."""
    
    data: dict = json.load(open('data.json', 'r'))
    
    f = data['first']
    m = data['mid']
    e = data['end']
    
    return (
        f[randint(0, len(f) - 1)],
        m[randint(0, len(m) - 1)],
        e[randint(0, len(e) - 1)],
    )

def submit(position, element) -> None:
    """Submit an element to the waiting list."""
    
    data = json.load(open('data.json', 'r'))
    
    element = element.strip().lower()
    
    # Already submited protection
    for el in data[('first', 'mid', 'end')[int(position) - 1]]:
        if el.lower() == element: return False
    
    data['waiting'].append({'position': position, 'element': element})
    
    # Write
    file = open('data.json', 'w')
    file.write(json.dumps(data))
    
    return True

def fetch() -> list:
    """Returns the list of the waiting submitions."""
    
    return json.load(open('data.json', 'r'))['waiting']

def remove(index) -> tuple:
    """Pop the element from the waiting list."""
    
    data = json.load(open('data.json', 'r'))
    data['waiting'].pop(index)
    
    file = open('data.json', 'w')
    file.write(json.dumps(data))

def accept(index) -> None:
    """Accept a submition."""
    
    # Get the element
    data = json.load(open('data.json', 'r'))
    el = data['waiting'].pop(index)
    data[('first', 'mid', 'end')[int(el['position']) - 1]].append(el['element'])
    
    # Write
    file = open('data.json', 'w')
    file.write(json.dumps(data))

def isTrigger(string: str) -> bool:
    """Returns wheter a string can be a trigger or not."""
    
    res = False
    
    for trigger in triggers:
        if trigger in string.lower(): res = True
        
    return res

# Create client
client = discord.Client()

# On start
@client.event
async def on_ready(): print('\033[1;0;1m[STARTED]\033[1;0;0m')

# On message
@client.event
async def on_message(msg):
    
    # Prevent the bot from responding to itself
    if msg.author.id == client.user.id: return
    
    content: str = msg.content

    # Pick a sentence and send it
    if isTrigger(content): await msg.channel.send(' '.join(pick()))
    
    # Submit an element
    elif content.startswith('!add'):
        # Add an element
        args = content.replace('!add ', '').split(' ')
        
        # Error protection
        if len(args) <= 1 or not args[0] in ('1', '2', '3'):
            return await msg.channel.send('Invalid syntax.')
        
        # Submit
        res = submit(args[0], ' '.join(args[1:]))
        
        # Send message
        if res: return await msg.channel.send('Submition saved. Thank you.')
        await msg.channel.send('This word is already in the list.')

    # Check elements
    elif content.startswith('!check'):
        
        # Role protection
        if not modRole in map(str, msg.author.roles):
            await msg.channel.send('Unauthorized user.')
            return
        
        # Returns each message
        fetched = fetch()
        raw = 'There is no submitions' if fetched is [] else 'Waiting submitions:'
        for i, el in enumerate(fetched): raw += f"\n{i+1}. {el['element']} (in {el['position']})"
        
        await msg.channel.send(raw)

    # Add or remove element
    elif content.startswith('!make'):
        args = content.replace('!make ', '').split(' ')
        
        # Role protection
        if not modRole in map(str, msg.author.roles):
            await msg.channel.send('Unauthorized user.')
            return
        
        if args[0] in ('rm', 'ok'): await msg.delete()
        
        if args[0] == 'rm':
            remove(int(args[1]) - 1)
            print(f'\033[1;0;7m- {args[1]}\033[1;0;0m')
            
            await msg.channel.send(f'Removed element {args[1]}.')
            
        elif args[0] == 'ok':
            accept(int(args[1]) - 1)
            print(f'\033[1;0;7m+ {args[1]}\033[1;0;0m')
            
            await msg.channel.send(f'Added element {args[1]}.')
            
        else: await msg.channel.send('Invalid syntax.')


# Run client
client.run(open('token', 'r').read())
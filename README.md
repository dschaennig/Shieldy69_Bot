# Shieldy69_Bot
A Bot against Telegram Spam-Accounts\
Can be used to have more direct control over spam-accounts that enter your Telegram group.

# Initialization
To initialize the bot, you need to add your own ```BotData.py``` file in the directory where your Bot runs.\
The ```BotData.py``` should look like this:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BotData class for Telegram Shield Bot
class Bot:
    
    def __init__(self, admins, token, group_id):
        self.muteList = []           # contains user_ids of banned users
        self.admins = admins         # contains user_ids of admins
        self.token = token           # will contain the bot token
        self.group_id = group_id     # will contain id of the targeted group

def setup():
    '''start the Bot with the data needed

    admins : [int]
    token : str
    group_id : int
    '''
    # before starting the bot you need to fill in this data
    bot = Bot(
        admins = [],\
        token = '',\
        group_id = 0
        )
    return(bot)
```

When you correctly fill in the admins, token and group_id, you're good to go, just launch the shieldy_main.py

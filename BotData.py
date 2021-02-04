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
    bot = Bot(admins, token, group_id)
    return(bot)
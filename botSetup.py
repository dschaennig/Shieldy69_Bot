#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''This module is just for simply starting the bot for the first time.

Here you can store the private data for the bot to start correctly'''

from BotData import Bot


def setup():
    '''start the Bot with the data needed

    admins : [int]
    token : str
    group_id : int
    '''
    # before starting the bot you need to fill in this data
    bot = Bot(admins, token, group_id)
    return(bot)
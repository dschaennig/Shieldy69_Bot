#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
        InlineQueryHandler
import pickle
import logging


class BotData:
    
    def __init__(self):
        self.muteList = [] # contains user_ids of banned users
        self.admins = [] # contains user_ids of admins
        self.token = None # will contain the bot token
        self.group_id = None # will contain id of the targeted group


def kick_member(update, context):
    '''Kick a member of your group chat through his user_id

    message format: '/kick <user_id>'
    for example:    '/kick <12345678>'

    Only works if the sender of this command is in the admin list of the bot
    
    '''

    # see if message / command is in the right format
    m_text = update.message.text
    try:
        id_kick = int(m_text[ m_text.find('<') + 1 : m_text.find('>') ])
    except:
        context.bot.send_message(
            chat_id = update.effective_chat.id,\
            text = "The command\n" + m_text +"\nwith its arguments is invalid"
            )
        return

    # load botdata ( muteList, admins, group_id )
    ml = pickle.load(open('botdata.pkl', 'rb'))

    # check if command comes from an admin
    if update.message.from_user.id not in ml.admins:
        context.bot.send_message(
            chat_id = update.effective_chat.id,\
            text = "You're not allowed to do that")    
        return
    
    # kick group member if everything is ok
    context.bot.kick_chat_member(
        chat_id = ml.group_id,\
        user_id = id_kick
        )
    del ml


def rem_mute_parse(update, context):
    '''unmute a member that was on the mute list through his user_id

    message format: '/rem_mute <user_id>'
    for example:    '/rem_mute <12345678>'

    Only works if the sender of this command is in the admin list of the bot

    '''

    # check format of the message / command
    m_text = update.message.text
    try:
        id_unmute = int(m_text[ m_text.find('<') + 1 : m_text.find('>') ])
    except:
        context.bot.send_message(
            chat_id = update.effective_chat.id,\
            text = "The command\n" + m_text +"\nwith its arguments is invalid"
            )
        return
            
    # load botdata (admins, muteList, group_id)        
    ml = pickle.load(open('botdata.pkl', 'rb'))

    # check if commander is admin
    if update.message.from_user.id not in ml.admins:
        context.bot.send_message(
            chat_id = update.effective_chat.id,\
            text = "You're not allowed to do that")    
        return
    
    #remove all instances of the id on the muteList
    while id_unmute in ml.muteList:
        ml.muteList.remove(id_unmute)
    
    # dump botdata with new muteList in the botdata.pkl file
    pickle.dump(ml, open('botdata.pkl', 'wb'), -1)
    del ml

    # send confirmation message
    context.bot.send_message(
        chat_id = update.effective_chat.id,\
        text = str(id_unmute) + " is no longer in the muteList"
        )


def text_checker(update, context):
    '''deals with all the messages that arent command, aka the messages that need to be scanned for spam

    '''

    # save all the data that could be needed
    m_text = update.message.text
    m_id = update.message.message_id
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id

    # load botdata (admins, muteList, group_id)
    ml = pickle.load( open('botdata.pkl', 'rb') )

    # check if user is already on the banlist
    # if then just delete the message
    if user_id in ml.muteList:
        context.bot.delete_message(
            chat_id = update.effective_chat.id,\
            message_id = m_id,\
            )
        del ml

    # if user isn't on banlist, search for keywords
    # here, "t.me/joinchat/" is a spam word and
    # "_exception_" allows "t.me/joinchat/" in a message
    elif ( "t.me/joinchat/" in m_text ) and ( '_exception_' not in m_text ):

        # contact each admin about ...
        for admin in ml.admins:
            # ... foward the spam message
            context.bot.forward_message(
                chat_id = admin,\
                from_chat_id = chat_id,\
                message_id = m_id
                )
            
            # ... send the spammers user id to unmute or kick them
            context.bot.send_message(
                chat_id = admin,\
                text = "User-ID des Spammers: " + str(user_id)
                )

        # delete the spam message
        context.bot.delete_message(
            chat_id = chat_id,\
            message_id = m_id,\
            )
        
        # if spammer isnt already in the spamlist, add them
        # (theoretically not needed, but safe is safe)
        if user_id not in ml.muteList:
            ml.muteList.append(user_id)
        pickle.dump(ml, open('botdata.pkl', 'wb'), -1)
        del ml


def get_chat_id(update, context):
    '''get chat_id of chat

    '''
    chat_id_asked = update.effective_chat.id
    context.bot.send_message(chat_id = chat_id_asked, \
            text = chat_id_asked)


def main():

    # load botdata for token at startup
    try:
        ml = pickle.load(open('botdata.pkl', 'rb'))
    except: # is only needed on the first start of the bot in a new enviroment
        ml = BotData()


        ml.admins = [62435438]
        # enter your bot-token here
        ml.token = '1584299429:AAF2uXeO6rcupQZuGAJKUKyCEkLOeLzMMhU'
        # enter your group-chat_id here
        ml.group_id = -1001255935478
        pickle.dump(ml, open('botdata.pkl', 'wb'), -1)

    global updater
    updater = Updater(token = ml.token ,\
            use_context = True)
    
    del ml

    dispatcher = updater.dispatcher

    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - \
            %(message)s', level = logging.INFO)


    # --------------------------------------------------------------
    # ------------------------ Commands ----------------------------
    # --------------------------------------------------------------
    kick_handler = CommandHandler('kick', kick_member)
    dispatcher.add_handler(kick_handler)

    remove_mute_handler = CommandHandler('rem_mute', rem_mute_parse)
    dispatcher.add_handler(remove_mute_handler)

    chat_id_handler = CommandHandler('chat_id', get_chat_id)
    dispatcher.add_handler(chat_id_handler)

    message_handler = MessageHandler(Filters.text, text_checker)
    dispatcher.add_handler(message_handler)
    # --------------------------------------------------------------
    # ------------------------ end Commands ------------------------
    # --------------------------------------------------------------


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
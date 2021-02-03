# Shieldy69_Bot
A Bot against Telegram Spam-Accounts\
Can be used to have more direct control over spam-accounts that enter your Telegram group.

# Initialization
To initialize the bot, you have to change the following lines of the bot in its main-function:
```python
    try:
        ml = pickle.load(open('botdata.pkl', 'rb'))
    except: # is only needed on the first start of the bot in a new enviroment
        ml = BotData()


        ml.admins = []
        # enter your bot-token here
        ml.token = ''
        # enter your group-chat_id here
        ml.group_id = 0
        pickle.dump(ml, open('botdata.pkl', 'wb'), -1)
```
Put the Telegram user_ids of those people into ```ml.admins = []``` that are supposed to be able to kick or unmute members.\
```user_id``` is an Integer type.\

Then enter your bot token at ```ml.token = ''``` and the chat_id of the group you want guarded at ```ml.group = 0```.\

After you have successfully started your bot once with these settings, you can redo the changes you did to the code as long as you
dont corrupt or delete the ```botdata.pkl``` file that gets created in the folder where the bot is running.

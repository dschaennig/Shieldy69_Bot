

# BotData class for Telegram Shield Bot
class Bot:
    
    def __init__(self):
        self.muteList = [] # contains user_ids of banned users
        self.admins = [] # contains user_ids of admins
        self.token = None # will contain the bot token
        self.group_id = None # will contain id of the targeted group
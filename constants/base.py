from socket import gethostname

# The channel id, can be found in telegram channel info, in this script, it should be @charoutv_bot
CHANNEL_ID = '@charontv_bot'

# The message to be sent to the channel
CHECKIN_MSG = '/checkin'

# Retry to varify the image that the channel send to you, default by 10
RETRY_TERMS = 10

# To choose use system enviroment or load the profile, default by False
USE_ENV = False

# Telethon client name, default value: hostname
CLIENT_NAME = gethostname()

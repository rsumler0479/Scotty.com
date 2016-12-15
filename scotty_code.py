import os
import time
import pyrebase
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
DATA_QUEST = "perform"



# instantiate Slack & Twilio clients

config = {
    "apiKey": "AIzaSyD3Z5y8TYvq75ewkwGzk5LqKUsjNNR7FQs",
    "authDomain": "notary-fb8b1.firebaseapp.com",
    "databaseURL": "https://notary-fb8b1.firebaseio.com",
    "storageBucket": "notary-fb8b1.appspot.com",
    "messagingSenderId": "903266716103"
}

firebase = pyrebase.initialize_app(config)



slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    
        #Receives commands directed at the bot and determines if they
        #are valid commands. If so, then acts on the commands. If not,
        #returns back what it needs for clarification.
    
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that O' captain my Captain. Sorry !" + \
        "Just a huge fan of Robin Williams."
        
    if command.startswith(DATA_QUEST):
        db = firebase.database()
        db.child("documents")
        return db 
                
    else:
        response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
                 "* command with numbers or letters, delimited by spaces."
            
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    
        # The Slack Real Time Messaging API is an events firehose.
        #this parsing function returns None unless a message is
        #directed at the Bot, based on its ID.
   
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Scotty connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
import os # imports specific operating system functionalities
from slackclient import SlackClient 
#retrieves the system routine SlackClient from library slackclient
                                    
                                     
                                       



BOT_NAME = 'scotty' # name of bot

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN')) 
# Accesses environment variables
                                                                  
                                                                  
if __name__ == "__main__": # Top Level Script Environment
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
         # retrieve  all users so we can find our bot 
         users = api_call.get('members')
         for user in users:
             if 'name' in user and user.get('name') == BOT_NAME:
                 print("BOT ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
     

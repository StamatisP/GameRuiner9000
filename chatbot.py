'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
import fun_funcs
import time
import string
import config

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        global userList
        #fun_funcs.threadedEvent("escape")
        userList = {}
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)


    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        #print(e)
        #print(e.arguments[0])
        #print(e.tags[3])
        #print(e.tags[3].get('value')) # THIS IS THE PERSONS NAME
        #print(e.arguments[0][:1])
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection
        user = e.tags[3].get('value')
        if len(e.arguments[0].split(' ')) == 1:
            argument = "nil"
        else:
            argument = e.arguments[0].split(' ')[1].upper()
        cooldown = 3
        if user not in userList:
            userList[user] = time.time() - 100
            #userList[user]['cooldown'] = time.time() - 1
        if time.time() > userList[user] + cooldown:
            # Poll the API to get current game.
            if cmd == "game":
                headers = {'Client-ID': self.client_id}
                stream_url = 'https://api.twitch.tv/helix/streams/?user_login=' + self.channel[1:]
                stream_r = requests.get(stream_url, headers=headers).json()
                if stream_r['data']:
                    user_url = 'https://api.twitch.tv/helix/users/?login=' + self.channel[1:]
                    user_r = requests.get(user_url, header=headers).json()
                    game_url = 'https://api.twitch.tv/helix/games/?id=' + stream_r['data'][0]['game_id']
                    game_r = requests.get(game_url, header=headers).json()
                    c.privmsg(self.channel,
                              user_r['data'][0]['display_name'] + ' is currently playing ' + game_r['data'][0]['name'])

            # Poll the API the get the current status of the stream
            elif cmd == "title":
                headers = {'Client-ID': self.client_id}
                stream_url = 'https://api.twitch.tv/helix/streams/?user_login=' + self.channel[1:]
                stream_r = requests.get(stream_url, headers=headers).json()
                if stream_r['data']:
                    user_url = 'https://api.twitch.tv/helix/users/?login=' + self.channel[1:]
                    user_r = requests.get(user_url, header=headers).json()
                    c.privmsg(self.channel,
                              user_r['data'][0]['display_name'] + ' channel title is currently ' + stream_r['data'][0][
                                  'title'])

            # Provide basic information to viewers for specific commands
            elif cmd == "test":
                message = "Test chat message."
                c.privmsg(self.channel, message)
            elif cmd == "jittermouse":
                message = "is jittering the mouse for 2 seconds!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("jitter")
            elif cmd == "lockmouse":
                message = "is locking the mouse for 5 seconds!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("lock")
            elif cmd == "leftclick":
                message = "is left clicking!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("lclick")
            elif cmd == "rightclick":
                message = "is right clicking!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("rclick")
            elif cmd == "ability":
                message = "Using ability!"
                print(user + " " + message)
                fun_funcs.randomAbility()
            elif cmd == "item":
                message = "Using item!"
                print(user + " " + message)
                fun_funcs.randomItem()
            elif cmd == "slowmouse":
                message = "is slowing the mouse down!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("slow")
            elif cmd == "weirdmouse":
                message = "is weirding out the mouse!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("bezier")
            elif cmd == "ger":
                message = "will make sure you never see the truth!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("zawarudo")
            elif cmd == "move":
                if argument != "LEFT" and argument != "RIGHT" and argument != "UP" and argument != "DOWN":
                    return
                message = "is moving you " + argument
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("move", argument)
            elif cmd == "dance":
                message = "is dancing!"
                if config.announcements: c.privmsg(self.channel, user + " " + message)
                print(user + " " + message)
                fun_funcs.threadedEvent("dance")

            # The command was not recognized
            else:
                # c.privmsg(self.channel, "Did not understand command: " + cmd)
                print("did not understand command: " + cmd)

            userList[user] = time.time()
        else:
            c.privmsg(self.channel, user + " is on cooldown for " + str(int((userList[user] + cooldown) - time.time())) + " more seconds!")
            #print(user + " is on cooldown!")
            #print(str(time.time()) + " " + str(userList[user] + cooldown))


def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
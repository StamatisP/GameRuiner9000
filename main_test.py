import chatbot
import config

bot = chatbot.TwitchBot(config.user, config.clientid, config.token, config.channel)
bot.start()


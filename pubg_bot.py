#PUBG Host Bot by PUBG Bot Developer Team
#----------------------------------------------------------------------- 
#
#Please install python-telegram-bot modules first!
#htps://github.com/python-telegram-bot/python-telegram-bot

#####################################################################################################################

#Importing Modules
try:
	import os, telegram, time, sys, logging
	from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
	from telegram.ext.dispatcher import run_async
	from functools import wraps
	from pprint import pprint
except ImportError as e:
	print("Problem: ",e)
	exit()

#Bot Data (Please insert bot token here!)
namebot = 'PUBG HOST BOT'
verbot  = 'v1' #<== You can change this version with your real bot version
tokenbot= '649674345:AAFTbhDPHxE1_uepOLfWMW2WIunFWXqHVcM' #<-- Put your bot token here!

#polling setup
try:
	updater= Updater(tokenbot)
except ValueError as e:
	print("Please insert your tokenbot!")
	exit()

#handling command
dispatcher = updater.dispatcher

#logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#####################################################################################################################
#DATA
#####################################################################################################################

#Temporary Data (I will use mysql soon!)
users_data = {}
vip_developer = 297620679
#####################################################################################################################
#COMMAND
#####################################################################################################################

#multithread handler
@run_async
#start command function
def start(bot, update):
	#avoid request from Grup (PM Only)
	if update.message.chat_id < 0:
		bot.send_message(chat_id=update.message.chat_id, text="_Use PM please!_", parse_mode=telegram.ParseMode.MARKDOWN)
		return

	#take user's username
	user= "`{}`".format(update.effective_user.username)
	#message
	msg = "*WELCOME TO PUBG Host Bot*!\n"
	msg+= "---------------------------------------\n"
	msg+= "Hello User "+user+" ! 😆\n"
	msg+= "My name Register Bot! You can register to me\n"
	msg+= "with\n`/register [pubg ign]`.\n"
	msg+= "\n"
	msg+= "More command:\n"
	msg+= "-> `/myid`\n"
	msg+= "\n"
	msg+= "For more information📚, you can ask:\n"
	msg+= "-> `@dharmaraj_24`\n"
	msg+= "-> `@Asaf31214`\n"
	msg+= "-> `@VrozAnims2003`\n"
	msg+= "---------------------------------------\n"
	#send message to user
	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

#multithread handler
@run_async
#register command function
def register(bot, update, args):
	#avoid request from grup (PM Only)
	if update.message.chat_id < 0:
		return
	#user data
	user_username = update.effective_user.username
	user_chatid   = update.message.chat_id
	user_firstname= update.message.from_user.first_name
	try:
		user_pubg_ign = args[0]
	except IndexError as e:
		update.message.reply_text("Please input your PUBG IGN!")
		return

	#filter for avoid spammer
	if len(user_pubg_ign) > 20:
		bot.send_message(chat_id=update.message.chat_id, text="*Please don't make spam in this bot!*", parse_mode=telegram.ParseMode.MARKDOWN)
		return

	#check same data:
	if str(user_chatid) in users_data:
		bot.send_message(chat_id=update.message.chat_id, text="*You has been registered!*", parse_mode=telegram.ParseMode.MARKDOWN)
		return

	#send user data to users_data
	users_data[str(user_chatid)]= {"user_firstname":str(user_firstname), "user_username":user_username, "user_pubg_ign":user_pubg_ign}

	#make report message about user's biodata
	msg = "PUBG PLAYER: "+user_firstname+"\n"
	msg+= "USERNAME  : @"+user_username+"\n"
	msg+= "PUBG IGN  : "+user_pubg_ign+"\n"

	print(users_data)
	print("\n")
	print(msg)

	#send message to user
	bot.send_message(chat_id=update.message.chat_id, text=msg)

@run_async
def myid(bot, update):
	if update.message.chat_id < 0:
		return

	chatid  = "`"+str(update.message.chat_id)+"`"
	msg 	= "*Your chat id*: "+chatid

	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def res(bot, update):
	global vip_developer

	if update.message.chat_id < 0:
		return

	elif update.message.chat_id >= 0:
		if update.message.chat_id == vip_developer:
			bot.send_message(chat_id=update.message.chat_id, text="Bot is restarting...")
			time.sleep(0.2)
			os.execl(sys.executable, sys.executable, *sys.argv)
			return

		elif update.message.chat_id != vip_developer:
			return

@run_async
def logout(bot, update):
	global vip_developer


#####################################################################################################################

#configure command
start_handler 	= CommandHandler('start', start)
register_handler= CommandHandler('register', register, pass_args=True)
myid_handler    = CommandHandler('myid', myid)
res_handler     = CommandHandler('res', res)

#####################################################################################################################

#set command

dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(myid_handler)
dispatcher.add_handler(res_handler)

#####################################################################################################################

#start polling
print(namebot,' ',verbot,' : Start!')
updater.start_polling()

#updater.idle() #untuk menjalankan heroku webhook

#####################################################################################################################
#FOR MORE INFORMATION, CHECK htps://github.com/python-telegram-bot/python-telegram-bot
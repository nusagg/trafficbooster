import telebot
import configparser
import subprocess
import threading

# Load config.ini
config = configparser.ConfigParser()
config.read('config.ini')

try:
    TOKEN = config['telegram']['bot_token']
    ADMIN_ID = int(config['telegram']['admin_id'])
except KeyError as e:
    print(f"Error: Key {e} tidak ditemukan di config.ini")
    exit(1)
except ValueError:
    print("Error: admin_id harus berupa angka")
    exit(1)

bot = telebot.TeleBot(TOKEN)
process = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.reply_to(message, "/run - Jalankan booster\n/status - Cek status\n/stop - Hentikan booster")

@bot.message_handler(commands=['run'])
def handle_run(message):
    if message.from_user.id != ADMIN_ID:
        return
    msg = bot.reply_to(message, "Masukkan target|threads|delay (contoh: https://site.com|10|2):")
    bot.register_next_step_handler(msg, run_booster)

def run_booster(message):
    global process
    if message.from_user.id != ADMIN_ID:
        return
    try:
        target, threads, delay = [x.strip() for x in message.text.split('|')]
        with open("target.txt", "w") as f:
            f.write(f"{target}\n{threads}\n{delay}")

        def start_process():
            global process
            process = subprocess.Popen(["python3", "booster.py"])

        threading.Thread(target=start_process).start()
        bot.send_message(message.chat.id, "Booster dimulai.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Gagal menjalankan booster: {e}")

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id != ADMIN_ID:
        return
    status = "Aktif" if process and process.poll() is None else "Tidak aktif"
    bot.send_message(message.chat.id, f"Status: {status}")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global process
    if message.from_user.id != ADMIN_ID:
        return
    if process:
        process.terminate()
        process = None
        bot.send_message(message.chat.id, "Booster dihentikan.")
    else:
        bot.send_message(message.chat.id, "Tidak ada booster yang berjalan.")

bot.polling()

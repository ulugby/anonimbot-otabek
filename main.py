from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import logging
import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokenini o'rnating va admin ID'ni belgilash
API_TOKEN = '7568431744:AAEHgMYL9KXcMMWt-YLo-djVefr58BH73Dk'
ADMIN_ID = [1395202672, ]  # Adminning Telegram ID sini bu yerga yozing
# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Start handler
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Salom! Menga xabar yuboring va men sizga javob beraman.")



# Foydalanuvchi ID'si orqali ma'lumot olish handleri
@dp.message(Command("finder"))
async def get_user_info(message: Message):
    if message.from_user.id in ADMIN_ID:
        # Foydalanuvchidan ID so'raladi (misol uchun /get_user_info 123456789)
        user_id = message.text.split()[1]  # ID ni split yordamida olish
        try:
            user = await bot.get_chat(user_id)
            keyboard = InlineKeyboardMarkup(row_width=1)  # row_width=1 bitta tugma bir qatorga
            button = InlineKeyboardButton(
                text="Foydalanuvchini ko'rish",
                url=f"https://t.me/{user.id}"
            )
            keyboard.add(button)  # Tugmani inline keyboardga qo'shish

            await message.answer(f"{user.first_name, user.last_name, user.username, user.id}", reply_markup=keyboard)

            # Foydalanuvchining shaxsiy ma'lumotlari
            user = await bot.get_chat(user_id)
            user_info = f"Foydalanuvchi haqida ma'lumot:\n"
            user_info += f"Ismi: {user.first_name} {user.last_name if user.last_name else ''}\n"
            user_info += f"Username: @{user.username if user.username else 'N/A'}\n"
            user_info += f"ID: {user.id}\n"

            # Foydalanuvchiga javob yuborish
            await message.answer("Foydalanuvchi haqida ma'lumot adminlarga yuborildi.")

        except Exception as e:
            await message.answer(f"Foydalanuvchi topilmadi: {e}")
    else:
        await message.answer("Sizda bu amalni bajarish huquqi yo'q.")


# Xabarlar handleri
@dp.message()
async def forward_message(message: Message):
    if message.from_user.id not in ADMIN_ID:
        # Foydalanuvchidan kelgan xabarni adminlarga yuborish
        for admin_id in ADMIN_ID:
                # Matnli xabar yuborish
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"#{message.from_user.id} : foydalanuvchi.\n\nYangi xabar: {message.text}"
                )

                # Agar xabarda rasm bo'lsa, rasm yuborish
                if message.photo:
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=message.photo[-1].file_id  # Eng oxirgi rasmni yuboradi
                    )

                # Agar xabarda video bo'lsa, video yuborish
                if message.video:
                    await bot.send_video(
                        chat_id=admin_id,
                        video=message.video.file_id  # Video fayl ID'si
                    )

                # Agar xabarda audio bo'lsa, audio yuborish
                if message.audio:
                    await bot.send_audio(
                        chat_id=admin_id,
                        audio=message.audio.file_id  # Audio fayl ID'si
                    )
                if message.voice:
                    await bot.send_voice(
                        chat_id=admin_id,
                        voice=message.voice.file_id  # Ovozli xabar fayl ID'si
                    )
        await bot.send_message(message.from_user.id, "Xabaringiz admin tomonidan ko'rib chiqiladi")
    if message.reply_to_message and message.reply_to_message.text:
        match = re.match(r"#(\d+)", message.reply_to_message.text)
        if match:
            rmatch = match.group(1)
            await bot.send_message(rmatch, message.text)
    # await bot.send_message(rmatch, message.text)


@dp.message()
async def reply_message(message: Message):
    print(message.reply_to_message)


# Asosiy funktsiyani ishga tushirish
if __name__ == '__main__':
    dp.run_polling(bot)
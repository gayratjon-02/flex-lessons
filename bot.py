from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.dispatcher import executor
import os
import moviepy.editor as mp

API_TOKEN = '7860336684:AAE5F3fIs49wGM59dqq5piZ8Zbg7Wrne9NA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Effektlar ro'yxati
EFFECTS = {
    "sepia": "Sepia Filter",
    "black_white": "Qora-oq Filter",
    "text_overlay": "Matn Qo'shish",
    "slow_motion": "Sekin Harakat"
}

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    # Videoni yuklab olish
    video_file = await bot.get_file(message.video.file_id)
    file_path = os.path.join("downloads", f"{message.from_user.id}.mp4")
    await video_file.download(destination_file=file_path)

    # Effektlar menyusini yuborish
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for effect in EFFECTS.values():
        keyboard.add(effect)
    await message.reply("Effekt tanlang:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in EFFECTS.values())
async def apply_effect(message: types.Message):
    user_id = message.from_user.id
    input_file = os.path.join("downloads", f"{user_id}.mp4")
    output_file = os.path.join("downloads", f"{user_id}_edited.mp4")

    # Tanlangan effektni qo'llash
    effect = message.text
    if effect == "Sepia Filter":
        clip = mp.VideoFileClip(input_file).fx(mp.vfx.colorx, 1.2).fx(mp.vfx.lum_contrast, 0, 50)
    elif effect == "Qora-oq Filter":
        clip = mp.VideoFileClip(input_file).fx(mp.vfx.blackwhite)
    elif effect == "Matn Qo'shish":
        clip = mp.VideoFileClip(input_file)
        txt_clip = mp.TextClip("Sizning Matningiz", fontsize=50, color='white')
        txt_clip = txt_clip.set_position('center').set_duration(clip.duration)
        clip = mp.CompositeVideoClip([clip, txt_clip])
    elif effect == "Sekin Harakat":
        clip = mp.VideoFileClip(input_file).fx(mp.vfx.speedx, 0.5)

    # Tahrirlangan videoni saqlash
    clip.write_videofile(output_file, codec='libx264')

    # Foydalanuvchiga yuborish
    await message.reply_video(InputFile(output_file))

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
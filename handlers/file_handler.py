from aiogram import Router, F
from aiogram.types import Message
from api.uploader import upload_file, track_job
import os

from handlers.login import USER_TOKENS

router = Router()

@router.message(F.document)
async def handle_file(message: Message):
    user_id = message.from_user.id
    client = USER_TOKENS.get(user_id)
    if not client:
        await message.answer("Вы не авторизованы. Используйте /login")
        return

    file_path = f"downloads/{message.document.file_name}"
    os.makedirs("downloads", exist_ok=True)
    file = await message.bot.get_file(message.document.file_id)
    await message.bot.download_file(file.file_path, file_path)

    await message.answer("Файл получен. Загружаю на сервер…")
    job_id = await upload_file(client, file_path)

    await message.answer(f"Задача создана: `{job_id}`\nСледим за статусом…", parse_mode="Markdown")

    async def on_status_update(data):
        await message.answer(f"Статус: {data['status']}")

    result_url = await track_job(job_id, on_status_update)
    await message.answer(f"Готово! Результат: {result_url}")

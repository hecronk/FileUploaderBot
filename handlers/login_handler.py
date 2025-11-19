from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from auth.client_auth import AuthClient

router = Router()
USER_TOKENS = {}  # хранение токенов per user

class LoginStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

# Команда /login
@router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    await state.set_state(LoginStates.waiting_for_username)
    await message.answer("Введите логин:")

# Ловим username
@router.message(
    LoginStates.waiting_for_username,
    F.text,
)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(LoginStates.waiting_for_password)
    await message.answer("Введите пароль:")

# Ловим пароль и логиним
@router.message(
    LoginStates.waiting_for_password,
    F.text,
)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text

    client = AuthClient()
    ok, token_or_error = await client.login(username, password)
    if ok:
        USER_TOKENS[message.from_user.id] = client
        await message.answer("Успешно авторизованы! Отправьте файл для загрузки")
    else:
        await message.answer(f"Ошибка авторизации: {token_or_error}")

    await state.clear()

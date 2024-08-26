from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.prof_keyboards import make_row_keyboard
from keyboards.keyboards import kb1



router = Router()


available_jobs = [
    'Программист',
    'Дизайнер',
    'Тестировщик'
]

available_grades = [
    'junoir',
    'middle',
    'senior'
]

available_work_formats = [
    'офис',
    'удаленка',
    'гибрид'
]

exit = ['выйти']


class ChoiceProfile(StatesGroup):
    job = State()
    grade = State()
    work_format = State()


@router.message(F.text.lower() == 'выйти')
async def exit_(message: types.Message, state: FSMContext):
    await message.answer("Вы вышли в главное меню", reply_markup=kb1)
    await state.clear()


@router.message(Command("prof"))
async def command_prof(message: types.Message, state: FSMContext):
    await message.answer(
        text="Выберите профессию",
        reply_markup=make_row_keyboard(available_jobs + exit)
    )
    await state.set_state(ChoiceProfile.job)


@router.message(ChoiceProfile.job, F.text.in_(available_jobs))
async def prof_chosen(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer(
        text="Выберите уровень",
        reply_markup=make_row_keyboard(available_grades + exit)
    )
    await state.set_state(ChoiceProfile.grade)


@router.message(ChoiceProfile.job)
async def prof_chosen_incorrect(message: types.Message):
    await message.answer(
        text="Выберите профессию",
        reply_markup=make_row_keyboard(available_jobs + exit)
    )


@router.message(ChoiceProfile.grade, F.text.in_(available_grades))
async def grade_chosen(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(
        text="Выберите формат работы",
        reply_markup=make_row_keyboard(available_work_formats + exit)
    )
    await state.set_state(ChoiceProfile.work_format)


@router.message(ChoiceProfile.grade)
async def grade_chosen_incorrect(message: types.Message):
    await message.answer(
        text="Выберите уровень",
        reply_markup=make_row_keyboard(available_grades + exit)
    )


@router.message(ChoiceProfile.work_format, F.text.in_(available_work_formats))
async def format_chosen(message: types.Message, state: FSMContext):
    await state.update_data(work_format=message.text)
    user_data = await state.get_data()
    await message.answer(f"Ваша профессия: {user_data['profession']}\nВаш уровень: {user_data['grade']}\nВаш формат работы: {user_data['work_format']}",
                        reply_markup=kb1)
    await state.clear()


@router.message(ChoiceProfile.work_format)
async def format_chosen_incorrect(message: types.Message):
    await message.answer(
        text="Выберите формат работы",
        reply_markup=make_row_keyboard(available_work_formats + exit)
    )
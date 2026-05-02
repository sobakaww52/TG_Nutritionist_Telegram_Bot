from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlmodel import select
from app.models.users import User


from app.bots.main.keyboards.inlines import get_start_keyboard
from app.database import async_session


router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):

    await message.delete()
    await state.clear()
    
    async with async_session() as session:
        result = await session.exec(select(User).where(User.telegram_id == message.from_user.id))
        user = result.first()

    if not user:
        text = f"""Здравствуйте! Благодарю за проявленный интерес к моему боту — это первый шаг к осознанному отношению к своему здоровью. 

Закрепите бота в своём чате, чтобы регулярно получать:

• актуальную информацию о профильных мероприятиях (вебинары, мастер‑классы, эфиры);

• научно обоснованные статьи по нутрициологии: разбор макро‑ и микронутриентов, их роли в поддержании энергии, качества сна и молодости организма;

• практические гайды: как составить сбалансированный рацион, оптимизировать режим дня и повысить качество жизни;

• эксклюзивные приглашения на образовательные события.

Составляй быстрее анкету, начни наполнятся энергией и двигаться к долгосрочным результатам — с заботой и наукой на вашей стороне 👇 """     
    
    else:
        text = f"""Здравствуйте {user.fio}!👋

Не забудьте закрепить бота в чате, чтобы получать:

• анонсы вебинаров, мастер‑классов и эфиров;

• полезные статьи о нутрициологии и питании;

• гайды по сбалансированному рациону и режиму дня;

• приглашения на эксклюзивные события.

Будем ставить фокус — на питании, восстановлении, энергии и долгосрочных результатах для вашего здоровья."""
               
    sent_msg = await message.answer(text, reply_markup=get_start_keyboard())                
    await state.update_data(last_msg_id=sent_msg.message_id)



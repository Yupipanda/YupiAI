from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from app.ai.aigentext import generate, gen_from_image
from app.ai.aisearch import aisearch_internet
from app.ai.aigenimage import generate_image
from app.ai.aimain import getfunc
from app.ai.scrape import scrape_url, split_user_inp
from app.utils.bbs import encode_image
from app.utils.text import answer_manipulate
from app.utils.allowed_users import ALLOWED_IDS
from app.utils.retry import retry_response
from datetime import datetime
from aiogram.types import FSInputFile
import os
from fuzzywuzzy import fuzz
from loguru import logger



rt = Router() 


@rt.message(F.text, F.text != '/start', F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS else None))
async def cmd_text(msg: Message):
    try:
        link = None
        func = await getfunc(msg.text)
        func = func.lstrip('[').rstrip(']')
        
        if '_scrape_url_' in func:
            link = func.split(', ')[1]
            result = await retry_response(func=scrape_url, text=link, mode='scrape', msg=msg)

        elif '_gen_text_' in func:
            result = await retry_response(func=generate, text=msg.text, mode='text', msg=msg)
           
        elif '_scrape_input_' in func:
            result = await retry_response(func=split_user_inp, text=msg.text, mode='scrape', msg=msg)
            
        elif '_gen_image_' in func:
            result = await retry_response(func=generate_image, text=msg.text, mode='image', msg=msg)
           
        elif '_search_in_inet_' in func:
            result = await retry_response(func=aisearch_internet, text=msg.text, mode='search_in_inet', msg=msg)
           
        else:
            result = await retry_response(func=generate, text=msg.text, mode='text', msg=msg)
            
        if 'gradio' not in result[0]:
           
            ddd = await answer_manipulate(result[0])
           
            if type(ddd) == list:
                for i in ddd:
                    if ddd[0] == i:
                        await msg.bot.edit_message_text(text=i, chat_id=msg.from_user.id, message_id=result[1])
                        #await msg.(text=i, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_to_message_id=result[1])
                    else:
                        await msg.reply(text=i)
                        #await msg.bot.answer(text=i, chat_id=msg.from_user.id, message_id=result[1])
            else:
                await msg.bot.edit_message_text(text=ddd, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, chat_id=msg.from_user.id, message_id=result[1])
        else:
            photo = FSInputFile(result[0])
            await msg.bot.delete_message(chat_id=msg.from_user, message_id=result[1])
            await msg.reply_photo(photo, reply_to_message_id=result[1])
            os.remove(result[0])
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')
    #for i in patterns_tuple:
    #    if fuzz.ratio(i[0], msg.text) >= 55:
    #        match i[1]:
    #            case 1:
    #                res = await ddg(msg.text)
    #    else:
    #        res = await generate(msg.text)
    #    ddd = await answer_manipulate(res)
    #if type(ddd) == list:
    #    for i in ddd:
    #        if ddd[0] == i:
    #            await msg.reply(text=i, parse_mode=ParseMode.MARKDOWN)
    #        else:
    #            await msg.answer(text=i, parse_mode=ParseMode.MARKDOWN)
    #else:
    #    await msg.reply(text=ddd, parse_mode=ParseMode.MARKDOWN)


#@rt.message(F.photo)
#async def phot(msg: Message):
#    podpis = msg.caption
#    photo = msg.photo
#    dd = str(datetime.now()).split(' ')
#    dttime = dd[0] + '_' + dd[1]
#    await msg.bot.download(photo[-1], destination=f'users_images/{dttime}.png')
#    ww = await gen_from_image(podpis, f'users_images/{dttime}.png')
#    ddd = await answer_manipulate(ww)
#    if type(ddd) == list:
#        for i in ddd:
#            if ddd[0] == i:
#                await msg.reply(text=i, parse_mode=ParseMode.MARKDOWN)
#            else:
#                await msg.answer(text=i, parse_mode=ParseMode.MARKDOWN)
#    else:
#        await msg.reply(text=ddd, parse_mode=ParseMode.MARKDOWN)
#    os.remove(f'users_images/{dttime}.png')

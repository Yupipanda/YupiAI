
async def retry_response(func, text, mode, msg):
    match mode:
        case 'text':
            await msg.reply('🥸 Погоди, генерирую ответ....')
        case 'image':
            await msg.reply('🎆 Погоди, генерирую картинку....')
        case 'scrape':
            await msg.reply('📝 Погоди, сокращаю....')
        case 'search_in_inet':
            await msg.reply('🌐 Погоди, ищу в инете....')
        case 'read_pdf':
            await msg.reply('📄 Погоди, читаю пдфку....')
    for i in range(3):
        result = await func(text)
        if result is not None:
            break
    if result is not None:
        return (result, msg.message_id+1)

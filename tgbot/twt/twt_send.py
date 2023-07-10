from PIL import Image, ImageDraw, ImageFont

def gen_twt_send(data):
    im = Image.open('tgbot/twt/send-start.jpg')
    
    font = ImageFont.truetype('tgbot/twt/aksans-250.otf', size=23)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (51, 24),
        data['phone_time'],
        font=font,
        fill='#f1ffff')
    
    data['tran_sum'] = '-' + data['tran_sum']
    data['tran_sum_usd'] = '≈ ' + data['tran_sum_usd'] + ' $'
    
    
    
    
    font = ImageFont.truetype('tgbot/twt/aksans-500.otf', size=48)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591 - int(font.getsize(data['tran_sum'])[0])) / 2, 145),
        data['tran_sum'],
        font=font,
        fill='#282a36')
    
    font = ImageFont.truetype('tgbot/twt/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591 - int(font.getsize(data['tran_sum_usd'])[0])) / 2, 214),
        data['tran_sum_usd'],
        font=font,
        fill='#79797b')
    
    # tran data and adress
    font = ImageFont.truetype('tgbot/twt/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((533 - int(font.getsize(data['date'])[0])), 280),
        data['date'],
        font=font,
        fill='#79797b')
    
    font = ImageFont.truetype('tgbot/twt/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((533 - int(font.getsize('Завершено')[0])), 345),
        'Завершено',
        font=font,
        fill='#79797b')
    
    font = ImageFont.truetype('tgbot/twt/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((533 - int(font.getsize(data['adress'])[0])), 405),
        data['adress'],
        font=font,
        fill='#79797b')
    
    # network
    font = ImageFont.truetype('tgbot/twt/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((533 - int(font.getsize(data['network'])[0])), 520),
        data['network'],
        font=font,
        fill='#79797b')
    
    
    # im.show()
    im.save(f'tgbot/twt/{data["user_id"]}_output_twt_send.png')
    
    
    
    
# data = {
#     'phone_time':'18:43',
#     'tran_sum':'13 USDT',
#     'tran_sum_usd':'13,00',
#     'date':'Сегодня, 18:30',
#     'adress':'TFQamj...9EhGVfy',
#     'network':'O TRX (0,00 $)',
#     'user_id':'654635654',
# }

# gen_twt_send(data)
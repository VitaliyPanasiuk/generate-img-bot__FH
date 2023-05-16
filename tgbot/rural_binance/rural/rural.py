from PIL import Image, ImageDraw, ImageFont

def gen_rural_png(data, time, user_id):
    im = Image.open('tgbot/rural_binance/rural/rural_png_start.png')
    
    font = ImageFont.truetype('tgbot/rural_binance/SFUIText-Semibold.ttf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (30, 23),
        time,
        font=font,
        fill='#131315')
    
    font = ImageFont.truetype('tgbot/rural_binance/ofont.ru_Roboto.ttf', size=18)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (108, 265),
        data['card_num'],
        font=font,
        fill='#7e7f7e')
    
    
    font = ImageFont.truetype('tgbot/rural_binance/aksans-250.otf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (25, 401),
        data['receiver_card'],
        font=font,
        fill='#131315')
    font = ImageFont.truetype('tgbot/rural_binance/aksans-250.otf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (25, 521),
        data['sum_tran'],
        font=font,
        fill='#131315')
    
    font = ImageFont.truetype('tgbot/rural_binance/aksans-250.otf', size=24)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (603 - int(font.getsize(data['sum_tran'])[0]), 661),
        data['commission'],
        font=font,
        fill='#131315')
    
    im.save(f'tgbot/rural_binance/rural/{user_id}_output_rural_png.png')
    
    
# time = '20:36'
# data = {
#     'card_num':'2200 38** **** 1831',
#     'receiver_card':'2200 70** **** 1932',
#     'sum_tran':'2 500,00 ₽',
#     'commission':'50,00 ₽',
# }

# gen_rural_png(data,time)
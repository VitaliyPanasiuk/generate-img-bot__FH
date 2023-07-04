from PIL import Image, ImageDraw, ImageFont


def gen_receipt_new_png(data,user_id):
    im = Image.open('tgbot/tn/tn_tn_new_start.png')

    font = ImageFont.truetype('tgbot/tn/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        data['time'],
        font=font,
        fill='#010200')

    font = ImageFont.truetype('tgbot/tn/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((52), 395),
        data['tn_time'],
        font=font,
        fill='#848484')


    font = ImageFont.truetype('tgbot/tn/aksans-500.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (591 - int(font.getsize(data['tran_sum'])[0] + 50), 420),
        data['tran_sum'],
        font=font,
        fill='#252525')


    font = ImageFont.truetype('tgbot/tn/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['tran_sum'])[0]), 601),
        data['tran_sum'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/tn/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['sender'])[0]), 644),
        data['sender'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/tn/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['card_receiver'])[0]), 687),
        data['card_receiver'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/tn/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['receiver'])[0]), 729),
        data['receiver'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/tn/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((170), 998),
        data['id_tran'],
        font=font,
        fill='#282828')


    im.save(f'tgbot/img/{user_id}_output_new_receipt_png.png')
    
# data_ex = {
#     'time' : '20:09',
#     'tn-time' : '18.01.2023 16:09:06',
#     'tran-sum' : '50 000 ₽',
#     'sender' : 'Александер Кеда',
#     'card_receiver' : '*5357',
#     'receiver' : 'Александр Т.',
#     'id-tran' : '1-7-406-442-603'
#     }
    
    
# gen_receipt(data_ex)
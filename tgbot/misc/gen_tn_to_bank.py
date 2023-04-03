from PIL import Image, ImageDraw, ImageFont


def gen_tn_to_bank(data,user_id):
    im = Image.open('tgbot/img/start_tn_to_bank.jpg')

    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        data['time'],
        font=font,
        fill='#fbfbf9')

    font = ImageFont.truetype('tgbot/img/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((52), 395),
        data['tn-time'],
        font=font,
        fill='#848484')

    dtf = data['tran-sum'].replace('₽', '').replace(' ', '')
    dts = data['comision'].replace('₽', '').replace(' ', '')
    sum = (int(dtf)) + (int(dts))
    sum = str('{0:,}'.format(sum).replace(',', ' ')) + ' ₽'
    
    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (591 - int(font.getsize(str(sum))[0] + 50), 420),
        sum,
        font=font,
        fill='#252525')


    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['tran-sum'])[0]), 601),
        data['tran-sum'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['comision'])[0]), 644),
        data['comision'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['sender'])[0]), 687),
        data['sender'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['card-receiver'])[0]), 729),
        data['card-receiver'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((170), 998),
        data['id-tran'],
        font=font,
        fill='#282828')

    im.save(f'tgbot/img/{user_id}_output_tn_to_bank.png')
    
# data_ex = {
#     'time' : '20:09',
#     'tn-time' : '18.01.2023 16:09:06',
#     'tran-sum' : '50 000 ₽',
#     'sender' : 'Александер Кеда',
#     'comision' : '1 400 ₽',
#     'card_receiver' : '220073******4862',
#     'id-tran' : '1-7-406-442-603'
#     }
    
    
# gen_tn_to_bank(data_ex)
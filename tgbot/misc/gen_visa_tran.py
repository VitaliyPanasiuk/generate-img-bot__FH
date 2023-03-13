from PIL import Image, ImageDraw, ImageFont


def gen_visa_tran(data,user_id):
    im = Image.open('tgbot/img/start-visa-tran.png')
    im1 = Image.open('tgbot/img/start-visa-tran.png')

    mask = Image.new('1', im1.size)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rectangle((0, 192, 591, 192+20), fill=1)



    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        data['time'],
        font=font,
        fill='#fefefe')

    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=26)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (295 - (int(font.getsize(data['tn_time'])[0]))/2, 212),
        data['tn_time'],
        font=font,
        fill='#f8f9fe')

    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=52)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (295 - (int(font.getsize(data['tran_sum'])[0]))/2, 530),
        data['tran_sum'],
        font=font,
        fill='#00c82e')


    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=24)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (295 - (int(font.getsize(data['tn_balance'])[0]))/2, 110),
        data['tn_balance'],
        font=font,
        fill='#4d4d4d')


    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=34)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (26, 161),
        'Траты за',
        font=font,
        fill='#4d4d4d')

    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=34)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (185, 161),
        data['tn_month'],
        font=font,
        fill='#0c2343')



    font = ImageFont.truetype('tgbot/img/aksans-050.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (371, 169),
        data['tn_month_spend'],
        font=font,
        fill='#0c2343')


    im = Image.composite(im1,im, mask)




    # im.show()
    im.save(f'tgbot/img/{user_id}_output_visa_tran.png')
    
    
# data_ex = {
#     'time' : '11:02',
#     'tn-time' : '13 февраля 2023, 20:40',
#     'tran-sum' : '+60 000 ₽',
#     'tn-balance' : '132 989 ₽',
#     'tn-month' : 'февраль',
#     'tn-month-spend' : '45 456 00 ₽'
# }
    
# gen_visa_tran(data_ex)
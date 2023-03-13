from PIL import Image, ImageDraw, ImageFont


def gen_donate(data,user_id):
    im = Image.open('tgbot/img/start-donate.png')

    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        data['time'],
        font=font,
        fill='#1b1b1b')

    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=26)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (295 - (int(font.getsize(data['tn_time'])[0]))/2, 93),
        data['tn_time'],
        font=font,
        fill='#21282e')

    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=52)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (295 - (int(font.getsize(data['tran_sum'])[0]))/2, 416),
        data['tran_sum'],
        font=font,
        fill='#00c82e')


    im.save(f'tgbot/img/{user_id}_output_donate.png')
    

# data_ex = {
#     'time' : '20:09',
#     'tn-time' : '10 февраля 2023, 20:40',
#     'tran-sum' : '+45 000 ₽',
# }

# gen_donate(data_ex)
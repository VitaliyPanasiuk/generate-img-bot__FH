from PIL import Image, ImageDraw, ImageFont

def gen_sber_sber_png(data,time_tran,time,user_id):
    im = Image.open('tgbot/sber/sber_sber_png/sber_sber_png_start.png')
    
    font = ImageFont.truetype('tgbot/sber/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        time,
        font=font,
        fill='#1b1b1b')
    
    font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591 / 2) - (int(font.getsize(time_tran)[0]) / 2), 188),
        time_tran,
        font=font,
        fill='#707070')
    
    start_height = 354
    
    for keys, values in data.items():
        if '₽' in values:
            values = values.replace('₽', '')
            
            font = ImageFont.truetype('tgbot/sber/aksans-regular.otf', size=22)
            draw_way = ImageDraw.Draw(im)
            draw_way.text(
                (55 + int(font.getsize(values)[0]) - 3, start_height - 3),
                '₽',
                font=font,
                fill='#000000')

            
        font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=22)
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (56, start_height),
            values,
            font=font,
            fill='#000000')
        
        if keys in ['receiver_card','commission']:
            start_height += 106
        else:
            start_height += 62
    
    # im.save('sber_sber_png/output_sber_sber_png.png')
    
    im.save(f'tgbot/sber/sber_sber_png/{user_id}_output_sber_sber_png.png')


    
    
    

# time = '01:32'
# time_tran = '16 апреля 2023 19:09:00 (МСК)'
# data = {
#     'fio_receiver':'Наталья Александровна М.',
#     'receiver_card':'**** 4578',
#     'fio_sender':'Ольга Владимировна Ш.',
#     'sender_card':'**** 2914',
#     'sum_tran':'18 000,00 ₽',
#     'commission':'0,00 ₽',
#     'num_tran':'4629107831',
#     'kod':'206790',
# }

# gen_sber_sber_png(data,time_tran,time)
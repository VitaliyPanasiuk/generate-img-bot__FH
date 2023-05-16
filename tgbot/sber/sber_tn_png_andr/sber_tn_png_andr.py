from PIL import Image, ImageDraw, ImageFont

def gen_sber_tn_png_andr(data,time_tran,time,user_id):
    im = Image.open('tgbot/sber/sber_tn_png_andr/sber_tn_png_andr_start.png')
    
    font = ImageFont.truetype('tgbot/sber/ofont.ru_Roboto.ttf', size=19)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (60, 11),
        time,
        font=font,
        fill='#f1ffff')
    
    font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591 / 2) - (int(font.getsize(time_tran)[0]) / 2), 188),
        time_tran,
        font=font,
        fill='#707070')
    
    start_height = 383
    
    for keys, values in data.items():
        if '₽' in values:
            values = values.replace('₽', '')
            
            font = ImageFont.truetype('tgbot/sber/aksans-regular.otf', size=22)
            draw_way = ImageDraw.Draw(im)
            draw_way.text(
                (66 + int(font.getsize(values)[0]) - 3, start_height - 3),
                '₽',
                font=font,
                fill='#000000')

            
        font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=22)
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (66, start_height),
            values,
            font=font,
            fill='#000000')
        
        
        start_height += 66
    
    im.save(f'tgbot/sber/sber_tn_png_andr/{user_id}_output_sber_tn_png_andr.png')
    
    
    
    
    
# time = '19:21'
# time_tran = '16 апреля 2023 19:09:00 (МСК)'
# data = {
#     'fio_receiver':'Наталья Александровна М.',
#     'receiver_card':'**** 4578',
#     'sum_tran':'5 000 ₽',
#     'commission':'75 ₽',
#     'final_sum':'5 075 ₽',
#     'sender_card':'**** 2914',
#     'receiver_contry':'РОССИЯ',
#     'receiver_bank':'Тинькофф БАНК',
#     'num_tran':'000S_0000000000299796940',
# }

# gen_sber_tn_png_andr(data,time_tran,time)
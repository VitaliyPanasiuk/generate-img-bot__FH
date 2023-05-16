from PIL import Image, ImageDraw, ImageFont

def gen_sber_sber_pdf(data,time_tran,user_id):
    im = Image.open('tgbot/sber/sber_sber/sber_sber_start_pdf.png')
    
    font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=33)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((834 / 2) - (int(font.getsize(time_tran)[0]) / 2), 202),
        time_tran,
        font=font,
        fill='#707070')
    
    start_height = 454
    
    for keys, values in data.items():
        if '₽' in values:
            values = values.replace('₽', '')
            
            font = ImageFont.truetype('tgbot/sber/aksans-regular.otf', size=33)
            draw_way = ImageDraw.Draw(im)
            draw_way.text(
                (55 + int(font.getsize(values)[0]) - 3, start_height - 3),
                '₽',
                font=font,
                fill='#000000')

            
        font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=33)
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (55, start_height),
            values,
            font=font,
            fill='#000000')
        
        if keys in ['receiver_card','commission']:
            start_height += 160
        else:
            start_height += 95
            
    
    im.save(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.png')
    image_1 = Image.open(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.png')
    im_1 = image_1.convert('RGB')
    im_1.save(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.pdf')

    
    
    
# time_tran = '19 апреля 2023 19:09:00 (МСК)'
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

# gen_sber_sber_pdf(data,time_tran)
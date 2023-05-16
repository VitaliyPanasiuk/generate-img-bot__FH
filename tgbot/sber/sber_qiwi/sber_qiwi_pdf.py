from PIL import Image, ImageDraw, ImageFont

def gen_sber_qiwi_pdf(data,time_tran,user_id):
    im = Image.open('tgbot/sber/sber_qiwi/sber-qiwi-pdf-start.png')
    
    font = ImageFont.truetype('tgbot/sber/ofont.ru_Arial.ttf', size=33)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((834 / 2) - (int(font.getsize(time_tran)[0]) / 2), 202),
        time_tran,
        font=font,
        fill='#707070')
    
    start_height = 327
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
        
        start_height += 105
    
    
    
    im.save(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.png')
    image_1 = Image.open(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.png')
    im_1 = image_1.convert('RGB')
    im_1.save(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.pdf')




# time_tran = '18 апреля 2023 19:24:58 мск'
# data = {
#     'sender':'НАТАЛИЯ ВАЛЕРЬЕВНА Б.',
#     'sender_card':'**** 1460',
#     'sum_tran':'1 500 ₽',
#     'commission':'30 ₽',
#     'final_sum':'1 530 ₽',
#     'receiver_card':'**** 4862',
#     'receiver_contry':'РОССИЯ',
#     'receiver_bank':'QIWI БАНК',
#     'prn_tran':'310814759234',
#     'num_tran':'000S_0000000000299796940',
# }

# gen_sber_qiwi_pdf(data,time_tran)
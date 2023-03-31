from PIL import Image, ImageDraw, ImageFont


def gen_receipt_pdf(data,user_id):
    im = Image.open('tgbot/img/start-receipt-pdf.png')

    # font = ImageFont.truetype('SFUIText-Semibold.ttf', size=22)
    # draw_way = ImageDraw.Draw(im)
    # draw_way.text(
    #     (33, 24),
    #     data['time'],
    #     font=font,
    #     fill='#1b1b1b')

    font = ImageFont.truetype('tgbot/img/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((42), 169),
        data['tn_time'],
        font=font,
        fill='#848484')


    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (591 - int(font.getsize(data['tran_sum'])[0] + 50), 194),
        data['tran_sum'],
        font=font,
        fill='#252525')


    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['tran_sum'])[0]), 375),
        data['tran_sum'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['sender'])[0]), 418),
        data['sender'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['card_receiver'])[0]), 461),
        data['card_receiver'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=18)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (540 - int(font.getsize(data['receiver'])[0]), 503),
        data['receiver'],
        font=font,
        fill='#505050')
    
    font = ImageFont.truetype('tgbot/img/aksans-050.otf', size=16)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((170), 772),
        data['id_tran'],
        font=font,
        fill='#282828')


    im.save(f'tgbot/img/{user_id}_output_receipt.png')
    image_1 = Image.open(f'tgbot/img/{user_id}_output_receipt.png')
    im_1 = image_1.convert('RGB')
    im_1.save(f'tgbot/img/{user_id}_output_receipt.pdf')
    
    
from PIL import Image, ImageDraw, ImageFont


def gen_tn_bank(data,user_id):
    im = Image.open('tgbot/img/start-tn-bank.jpg')
    
    font = ImageFont.truetype('tgbot/img/SFUIText-Semibold.ttf', size=22)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (33, 24),
        data['time'],
        font=font,
        fill='#050507')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=32)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (72, 343),
        data['balance'],
        font=font,
        fill='#252527')
    
    balance = data['balance'].replace("₽", '').replace(" ", '').replace(",", '.')
    tran_sum = data['tran_sum'].replace("₽", '').replace(" ", '').replace(",", '.')
    mn = float(balance) - int(tran_sum)
    mn = str(round(mn, 2))
    mn += ' ₽'
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=32)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (334, 343),
        mn.replace(".", ','),
        font=font,
        fill='#252527')
    
    font = ImageFont.truetype('tgbot/img/aksans-500.otf', size=64)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (164, 395),
        data['tran_sum'],
        font=font,
        fill='#252527')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=32)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591/2) - (int(font.getsize(data['tn_name'])[0])/2), 530),
        data['tn_name'],
        font=font,
        fill='#252527')
    
    font = ImageFont.truetype('tgbot/img/aksans-250.otf', size=32)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        ((591/2) - (int(font.getsize(data['card_num'])[0])/2), 748),
        data['card_num'],
        font=font,
        fill='#252527')
    
    
    
    im.save(f'tgbot/img/{user_id}_output_tn_bank.png')
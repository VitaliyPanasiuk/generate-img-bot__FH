from PIL import Image, ImageDraw, ImageFilter, ImageFont

def gen(data):
    
    if float(data['pnl'].replace(',','.')) >= 0:
        im = Image.open('tgbot/pnl_okx/start_plus.jpg')
    else:
        im = Image.open('tgbot/pnl_okx/start_minus.jpg')
    im2 = Image.open(f'tgbot/pnl_okx/{data["user_id"]}_ava.jpg').resize((75, 75))
    
    # draw img and name
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, im2.size[0], im2.size[1]), fill=255) #75 75
        
    # back_im = im1.copy()
    im.paste(im2, (54, 158), mask_im)
    
    font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (144, 182),
        data['name'],
        font=font,
        fill='#f9f9f9')
    
    # draw pair and laverage
    text = data['pair'] + ' Бессрочные'
    font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=30)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (54, 303),
        text,
        font=font,
        fill='#f9f9f9')
    
    if data['way'].lower() == 'купить':
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=26)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (54, 363),
            'Купить',
            font=font,
            fill='#18ad49')
        text = data['pair'] + ' Бессрочные'
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=26)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (182, 363),
            data['leverage'],
            font=font,
            fill='#18ad49')
        
        h_line = Image.open('tgbot/pnl_okx/h-line.png')
        im.paste(h_line, (160, 361))
    else:
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=26)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (54, 363),
            'Продать',
            font=font,
            fill='#cc4b69')
        text = data['pair'] + ' Бессрочные'
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=26)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (203, 363),
            data['leverage'],
            font=font,
            fill='#cc4b69')
        
        h_line = Image.open('tgbot/pnl_okx/h-line.png')
        im.paste(h_line, (180, 361))
    
    if float(data['pnl'].replace(',','.')) >= 0:        
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=100)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (50, 517),
            data['pnl'],
            font=font,
            fill='#18ad49')
        
        gper = Image.open('tgbot/pnl_okx/gper.png')
        im.paste(gper, (50 + int(font.getsize(data['pnl'])[0]) + 30, 517),gper)
    else:
        font = ImageFont.truetype('tgbot/pnl_okx/aksans-250.otf', size=100)#error
        draw_way = ImageDraw.Draw(im)
        draw_way.text(
            (50, 517),
            data['pnl'],
            font=font,
            fill='#cc4b69')
        
        rper = Image.open('tgbot/pnl_okx/rper.png')
        im.paste(rper, (50 + int(font.getsize(data['pnl'])[0]) + 30, 517),rper)
    
    font = ImageFont.truetype('tgbot/pnl_okx/SFUIText-Light.ttf', size=26)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (71, 714),
        data['entry-p'],
        font=font,
        fill='#f9f9f9')
    
    font = ImageFont.truetype('tgbot/pnl_okx/SFUIText-Light.ttf', size=26)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (298, 714),
        data['now-p'],
        font=font,
        fill='#f9f9f9')
    
    font = ImageFont.truetype('tgbot/pnl_okx/SFUIText-Light.ttf', size=40)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (1075 - int(font.getsize(data['ref'])[0]), 650),
        data['ref'],
        font=font,
        fill='#f9f9f9')
    
    mes = 'Отправлено ' + data['date']
    font = ImageFont.truetype('tgbot/pnl_okx/SFUIText-Light.ttf', size=26)#error
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (1075 - int(font.getsize(mes)[0]), 712),
        mes,
        font=font,
        fill='#828282')
    
    
    im.save(f'tgbot/pnl_okx/{data["user_id"]}_output.jpg', quality=95)
    
    

data_ex = {
    'img' : 'ava2.jpg',
    'name' : 'TimeIsMoneyKR',
    'pair' : 'AGLDUSDT',
    'way' : 'купить',
    'leverage' : '30,00x',
    'pnl' : '+8,05',
    'entry-p' : '0,1101',
    'now-p' : '0,1097',
    'ref' : '13273638',
    'date' : '31.07.2023, 21:42:18',
}

# gen(data_ex)

from PIL import Image, ImageDraw, ImageFont



def generate_minus(user_data):
    print(user_data['lavarage'])
    
    x = user_data['lavarage'].replace("x", "").replace("X", "").replace("х", "").replace("Х", "")
    # x = user_data['lavarage']
    # x = user_data['lavarage']
    # x = user_data['lavarage']
    profit2 = user_data['profit'].replace(',','.').replace('-','')
    
    if float(profit2)>50:
        im = Image.open('tgbot/pnl/start-s-minus.jpg')
    else:
        im = Image.open('tgbot/pnl/start-f-minus.jpg')
    w = True
    

    if user_data['way'].lower() == 'купить':
        way_color = '#24be82'
        way = 'Купить'
    else:
        way_color = '#d55169'
        way = 'Продать'

    lav = 0
    for i in user_data['lavarage']:
        lav = lav + 1

    if w == False:
        lav_dist = 387
        # lav_dist = 413
    else:
        lav_dist = 406
        # lav_dist = 408

    currency = user_data['currency'].upper() + ' ' + 'Бессрочный'

    font = ImageFont.truetype('tgbot/pnl/SFUIDisplay-Regular.ttf', size=42)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (187, 255),
        way,
        font=font,
        fill=way_color)

    font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=32)
    draw_lev = ImageDraw.Draw(im)
    draw_lev.text(
        (456 - int((int(font.getsize(x.lower())[0]) / 2)), 263),
        x.lower(),
        font=font,
        fill='#f8f4f3')
    lavx = Image.open('tgbot/pnl/x.png')
    im.paste(lavx, (456 + int((int(font.getsize(x.lower())[0]) / 2)) + 3, 272), lavx)

    font = ImageFont.truetype('tgbot/pnl/SFUIText-Semibold.ttf', size=42)
    draw_cur = ImageDraw.Draw(im)
    if w == True:
        draw_cur.text(
            (605, 255),
            currency,
            font=font,
            fill='#f8f4f3')
    else:
        # draw_cur.text(
        #         (553, 258),
        #         currency,
        #         font=font,
        #         fill='#f8f4f3')

        start_length = 553
        for i in currency:
            draw_cur.text(
                (start_length, 258),
                i,
                font=font,
                fill='#f8f4f3')
            start_length += int(font.getsize(i)[0])-3
            
    font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=46)
    draw_lev = ImageDraw.Draw(im)
    draw_lev.text(
        (331, 681),
        user_data['ref'].lower(),
        font=font,
        fill='#f8f4f3')
    profit = user_data['profit'].replace(',','.')
    
    if float(profit) > 0:
        font = ImageFont.truetype(
            'tgbot/pnl/bin-SVG.ttf', size=92)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (223, 350),
            user_data['profit'].lower(),
            font=font,
            fill='#32c285')
        Gplus = Image.open('tgbot/pnl/plus.png')
        Gper = Image.open('tgbot/pnl/per.png')
    else:
        font = ImageFont.truetype(
            'tgbot/pnl/bin-SVG.ttf', size=92)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (223, 350),
            user_data['profit'].lower(),
            font=font,
            fill='#d55169')
        Gplus = Image.open('tgbot/pnl/minus.png')
        Gper = Image.open('tgbot/pnl/per-red.png')


    
    
    im.paste(Gplus, (165, 375), Gplus)
    im.paste(Gper, (223 + 11 + int(font.getsize(user_data['profit'])[0]), 332), Gper)
    
    
    
    if w == True:
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (549, 478),
            user_data['fprice'].lower(),
            font=font,
            fill='#dfb841')
        
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (549, 522),
            user_data['sprice'].lower(),
            font=font,
            fill='#dfb841')
        # price_dist = 537
    else:
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (596, 478),
            user_data['fprice'].lower(),
            font=font,
            fill='#dfb841')
        
        
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (596, 522),
            user_data['sprice'].lower(),
            font=font,
            fill='#dfb841')
        # price_dist = 584
    
    im.save(f'tgbot/pnl/{user_data["user_id"]}_output_pnl.png')
    

def generate_plus(user_data):
    print(user_data['lavarage'])
    
    x = user_data['lavarage'].replace("x", "").replace("X", "").replace("х", "").replace("Х", "")
    # x = user_data['lavarage']
    # x = user_data['lavarage']
    # x = user_data['lavarage']
    profit2 = user_data['profit'].replace(',','.').replace('-','')
    
    if float(profit2)>50:
        im = Image.open('tgbot/pnl/start-s-plus.jpg')
    else:
        im = Image.open('tgbot/pnl/start-f-plus.jpg')
    
    w = True
    

    if user_data['way'].lower() == 'купить':
        way_color = '#24be82'
        way = 'Купить'
    else:
        way_color = '#d55169'
        way = 'Продать'

    lav = 0
    for i in user_data['lavarage']:
        lav = lav + 1

    if w == False:
        lav_dist = 387
        # lav_dist = 413
    else:
        lav_dist = 406
        # lav_dist = 408

    currency = user_data['currency'].upper() + ' ' + 'Бессрочный'

    font = ImageFont.truetype('tgbot/pnl/SFUIDisplay-Regular.ttf', size=42)
    draw_way = ImageDraw.Draw(im)
    draw_way.text(
        (187, 255),
        way,
        font=font,
        fill=way_color)

    font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=32)
    draw_lev = ImageDraw.Draw(im)
    draw_lev.text(
        (486 - int((int(font.getsize(x.lower())[0]) / 2)), 263),
        x.lower(),
        font=font,
        fill='#f8f4f3')
    lavx = Image.open('tgbot/pnl/x.png')
    im.paste(lavx, (486 + int((int(font.getsize(x.lower())[0]) / 2)) + 3, 272), lavx)

    font = ImageFont.truetype('tgbot/pnl/SFUIText-Semibold.ttf', size=42)
    draw_cur = ImageDraw.Draw(im)
    if w == True:
        draw_cur.text(
            (625, 255),
            currency,
            font=font,
            fill='#f8f4f3')
    else:
        # draw_cur.text(
        #         (553, 258),
        #         currency,
        #         font=font,
        #         fill='#f8f4f3')

        start_length = 553
        for i in currency:
            draw_cur.text(
                (start_length, 258),
                i,
                font=font,
                fill='#f8f4f3')
            start_length += int(font.getsize(i)[0])-3
            
    font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=46)
    draw_lev = ImageDraw.Draw(im)
    draw_lev.text(
        (331, 681),
        user_data['ref'].lower(),
        font=font,
        fill='#f8f4f3')
    
    profit = user_data['profit'].replace(',','.')
    
    if float(profit) > 0:
        font = ImageFont.truetype(
            'tgbot/pnl/bin-SVG.ttf', size=92)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (223, 350),
            user_data['profit'].lower(),
            font=font,
            fill='#32c285')
        Gplus = Image.open('tgbot/pnl/plus.png')
        Gper = Image.open('tgbot/pnl/per.png')
    else:
        font = ImageFont.truetype(
            'tgbot/pnl/bin-SVG.ttf', size=92)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (223, 350),
            user_data['profit'].lower(),
            font=font,
            fill='#d55169')
        Gplus = Image.open('tgbot/pnl/minus.png')
        Gper = Image.open('tgbot/pnl/per-red.png')


    
    
    im.paste(Gplus, (165, 375), Gplus)
    im.paste(Gper, (223 + 11 + int(font.getsize(user_data['profit'])[0]), 332), Gper)
    
    
    
    if w == True:
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (549, 478),
            user_data['fprice'].lower(),
            font=font,
            fill='#dfb841')
        
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (549, 522),
            user_data['sprice'].lower(),
            font=font,
            fill='#dfb841')
        # price_dist = 537
    else:
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (596, 478),
            user_data['fprice'].lower(),
            font=font,
            fill='#dfb841')
        
        
        font = ImageFont.truetype(
        'tgbot/pnl/bin-SVG.ttf', size=30)
        draw_lev = ImageDraw.Draw(im)
        draw_lev.text(
            (596, 522),
            user_data['sprice'].lower(),
            font=font,
            fill='#dfb841')
        # price_dist = 584
    
    im.save(f'tgbot/pnl/{user_data["user_id"]}_output_pnl.png')
    
user_data = {
    'lavarage' : '24x',
    'way' : 'Купить',
    'currency' : 'SUSHIUSDT',
    'profit' : '-0,69',
    'fprice' : '0,6943',
    'sprice' : '0,6941',
    'ref' : '143491686',
    'user_id' : '4435345345',
}

    
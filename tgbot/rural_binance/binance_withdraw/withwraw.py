from PIL import Image, ImageDraw, ImageFont
import textwrap

def split_text_by_width(text, max_width, font_size, font_path):
    image = Image.new("RGB", (1, 1))  # Создаем изображение размером 1x1 пиксель
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    lines = []
    current_line = ""
    
    for word in list(text):
        word_width = draw.textsize(word, font=font)[0]
        
        if draw.textsize(current_line + "" + word, font=font)[0] <= max_width:
            current_line += "" + word
        else:
            lines.append(current_line.strip())
            current_line = word
    
    lines.append(current_line.strip())
    
    return lines

def generate_withdraw(data, user_id):
    deposit = Image.open('tgbot/rural_binance/binance_withdraw/withdraw_start.png')
    
    usdt = Image.open('tgbot/rural_binance/binance_withdraw/usdt.png')
    tr = Image.open('tgbot/rural_binance/binance_withdraw/tr.png')
    colon = Image.open('tgbot/rural_binance/binance_withdraw/colon.png')
    

    #отрисовка времени на телефоне 
    
    font = ImageFont.truetype('tgbot/rural_binance/SFUIText-Semibold.ttf', size=23)
    draw_way = ImageDraw.Draw(deposit)
    draw_way.text(
		(44, 23),
		data['time'],
		font=font,
		fill='#232532')
    
    # отрисока сети перевода
    font = ImageFont.truetype('tgbot/rural_binance/ofont.ru_Roboto.ttf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
        (566 - int(font.getsize(data['network'])[0]), 646),
        data['network'],
        font=font,
        fill='#232532')
    
    # отрисовка комисси сети
    data['commission'] = data['commission'] + ' USDT'
    
    font = ImageFont.truetype('tgbot/rural_binance/ofont.ru_Roboto.ttf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
        (566 - int(font.getsize(data['commission'])[0]), 895),
        data['commission'],
        font=font,
        fill='#232532')
    
    # разбиение даты на элементы
    time_value2 = data['date'].split(' ')
    tm_date = time_value2[0]
    tm_time = time_value2[1]
    
    tm_date = tm_date.split('-')
    tm_time = tm_time.split(':')
    
    # отрисовка разбитой даты
    font = ImageFont.truetype(
    'tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374, 949),
    	tm_date[0],
    	font=font,
    	fill='#232532')
    deposit.paste(tr, (374+int(font.getsize(tm_date[0])[0])+2, 953), mask=tr.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374+int(font.getsize(tm_date[0])[0])+10, 949),
    	tm_date[1],
    	font=font,
    	fill='#232532')
    deposit.paste(tr, (374+int(font.getsize(tm_date[0])[0])+10+int(font.getsize(tm_date[1])[0])+2, 953), mask=tr.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+20, 949),
    	tm_date[2],
    	font=font,
    	fill='#232532')
    # new date
    width_for_time = 374+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+int(font.getsize(tm_date[2])[0])+27
    font = ImageFont.truetype(
    	'tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time, 949),
    	tm_time[0],
    	font=font,
    	fill='#232532')
    deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+3, 949), mask=colon.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time+int(font.getsize(tm_time[0])[0])+9, 949),
    	tm_time[1],
    	font=font,
    	fill='#232532')
    deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+9+int(font.getsize(tm_time[1])[0])+3, 949), mask=colon.convert('RGBA'))
    font = ImageFont.truetype('tgbot/rural_binance/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time+int(font.getsize(tm_time[0])[0])+int(font.getsize(tm_time[1])[0])+18, 949),
    	tm_time[2],
    	font=font,
    	fill='#232532')
    
    
    
    # отрисовка суммы перевода
    font = ImageFont.truetype('tgbot/rural_binance/binance.ttf', size=31)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(int(292-((int(font.getsize(data['amount'])[0]) + 8 + 54)/2)), 250),
    	data['amount'],
    	font=font,
    	fill='#232532')
    
    deposit.paste(usdt, (int(292-((int(font.getsize(data['amount'])[0]) + 8 + 54)/2) + int(font.getsize(data['amount'])[0]) + 10), 254), mask=usdt.convert('RGBA'))

    # draw address
    font = ImageFont.truetype('tgbot/rural_binance/ofont.ru_Roboto.ttf', size=20)
    lines = split_text_by_width(data['address'],277,20,'tgbot/rural_binance/ofont.ru_Roboto.ttf')
    # lines = textwrap.wrap(data['address'], width=23)
    
    start_y = 700
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (244 + (277 - int(font.getsize(line)[0])), start_y),
            line,
            font=font,
            fill='#232532')
        
        start_y += 28
        
    # draw txid
    font = ImageFont.truetype('tgbot/rural_binance/ofont.ru_Roboto.ttf', size=20)
    lines = split_text_by_width(data['txid'],277,20,'tgbot/rural_binance/ofont.ru_Roboto.ttf')
    # lines = textwrap.wrap(data['txid'], width=23)
    
    start_y = 787
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (244 + (277 - int(font.getsize(line)[0])), start_y),
            line,
            font=font,
            fill='#232532')
        draw_lev.line((244 + (277 - int(font.getsize(line)[0])),start_y + 23, 523 ,start_y + 23), fill='#232532', width=2)
        start_y += 28
    
    deposit.save(f'tgbot/rural_binance/binance_withdraw/{user_id}_output_withdraw.png')
     
# net - 2,3,4
# wifi - 1,2,3
# battery - 10,20,50,90
# data = {
#     'time':'20:49',
#     'amount':'400',
#     'network':'TRX',
#     'address':'TTq4GUFGAh2a9VAzabsMfyaqZB8KTd9bim',
#     'txid':'9ece3c91c3d7a3889fe1afebd21fb4c2ce7200ecd28ed54f83971cbd3e5f037f',
#     'commission':'1',
#     'date':'2023-04-27 20:41:05',
#     'user_id':'5468686',
# }
    
# generate_withdraw(data)
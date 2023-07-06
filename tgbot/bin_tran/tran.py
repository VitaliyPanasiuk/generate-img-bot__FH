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

def generate_bin_tran(data):
    deposit = Image.open('tgbot/bin_tran/ex-start.jpg')
    
    usdt = Image.open('tgbot/bin_tran/busd.png')
    tr = Image.open('tgbot/bin_tran/tr.png')
    colon = Image.open('tgbot/bin_tran/colon.png')
    
    font = ImageFont.truetype('tgbot/bin_tran/SFUIText-Semibold.ttf', size=23)
    draw_way = ImageDraw.Draw(deposit)
    draw_way.text(
		(44, 18),
		data['time'],
		font=font,
		fill='#22272a')
    
    # разбиение даты на элементы
    time_value2 = data['date'].split(' ')
    tm_date = time_value2[0]
    tm_time = time_value2[1]
    
    tm_date = tm_date.split('-')
    tm_time = tm_time.split(':')
    
    # отрисовка разбитой даты
    font = ImageFont.truetype(
    'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374, 792),
    	tm_date[0],
    	font=font,
    	fill='#161b1f')
    deposit.paste(tr, (374+int(font.getsize(tm_date[0])[0])+2, 796), mask=tr.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374+int(font.getsize(tm_date[0])[0])+10, 792),
    	tm_date[1],
    	font=font,
    	fill='#161b1f')
    deposit.paste(tr, (374+int(font.getsize(tm_date[0])[0])+10+int(font.getsize(tm_date[1])[0])+2, 796), mask=tr.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(374+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+20, 792),
    	tm_date[2],
    	font=font,
    	fill='#161b1f')
    # new date
    width_for_time = 374+int(font.getsize(tm_date[0])[0])+int(font.getsize(tm_date[1])[0])+int(font.getsize(tm_date[2])[0])+27
    font = ImageFont.truetype(
    	'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time, 792),
    	tm_time[0],
    	font=font,
    	fill='#161b1f')
    deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+3, 792), mask=colon.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time+int(font.getsize(tm_time[0])[0])+9, 792),
    	tm_time[1],
    	font=font,
    	fill='#161b1f')
    deposit.paste(colon, (width_for_time+int(font.getsize(tm_time[0])[0])+9+int(font.getsize(tm_time[1])[0])+3, 792), mask=colon.convert('RGBA'))
    font = ImageFont.truetype(
    	'tgbot/bin_tran/binance2.ttf', size=16)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(width_for_time+int(font.getsize(tm_time[0])[0])+int(font.getsize(tm_time[1])[0])+18, 792),
    	tm_time[2],
    	font=font,
    	fill='#161b1f')
    
    
    
    # отрисовка суммы перевода
    font = ImageFont.truetype('tgbot/bin_tran/binance.ttf', size=31)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(int(292-((int(font.getsize(data['amount'])[0]) + 8 + 54)/2)), 231),
    	data['amount'],
    	font=font,
    	fill='#161b1f')
    
    font = ImageFont.truetype('tgbot/bin_tran/ofont.ru_Roboto.ttf', size=31)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(int(295 + (int(font.getsize(data['amount'])[0])/2)), 221),
    	data['coin'],
    	font=font,
    	fill='#161b1f')
    
    # deposit.paste(usdt, (int(292-((int(font.getsize(data['amount'])[0]) + 8 + 54)/2) + int(font.getsize(data['amount'])[0]) + 10), 235), mask=usdt.convert('RGBA'))

    # draw address
    font = ImageFont.truetype('tgbot/bin_tran/ofont.ru_Roboto.ttf', size=20)
    lines = split_text_by_width(data['address'],277,20,'tgbot/bin_tran/ofont.ru_Roboto.ttf')
    # lines = textwrap.wrap(data['address'], width=23)
    
    start_y = 607
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (244 + (277 - int(font.getsize(line)[0])), start_y),
            line,
            font=font,
            fill='#161b1f')
        
        start_y += 28
        
    # draw txid
    font = ImageFont.truetype('tgbot/bin_tran/ofont.ru_Roboto.ttf', size=20)
    lines = split_text_by_width(data['txid'],277,20,'tgbot/bin_tran/ofont.ru_Roboto.ttf')
    # lines = textwrap.wrap(data['txid'], width=23)
    
    start_y = 682
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (244 + (277 - int(font.getsize(line)[0])), start_y),
            line,
            font=font,
            fill='#161b1f')
        draw_lev.line((244 + (277 - int(font.getsize(line)[0])),start_y + 23, 523 ,start_y + 23), fill='#161b1f', width=2)
        start_y += 28
        
    # confirmations
    font = ImageFont.truetype('tgbot/bin_tran/ofont.ru_Roboto.ttf', size=20)
    draw_lev.text(
            (568 - int(font.getsize(data['conf'])[0]), 454),
            data['conf'],
            font=font,
            fill='#161b1f')
    # netwoek
    font = ImageFont.truetype('tgbot/bin_tran/ofont.ru_Roboto.ttf', size=20)
    draw_lev.text(
            (568 - int(font.getsize(data['network'].upper())[0]), 558),
            data['network'].upper(),
            font=font,
            fill='#161b1f')
    
    # deposit.show()
    deposit.save(f'tgbot/bin_tran/{data["user_id"]}_output_tran.png')
     

# data = {
#     'amount':'4983,94858391',
#     'conf':'20 / 15 / 0',
#     'network':'BSC',
#     'address':'TTq4GUFGAh2a9VAzabsMfyaqZB8KTd9bim',
#     'txid':'9ece3c91c3d7a3889fe1afebd21fb4c2ce7200ecd28ed54f83971cbd3e5f037f',
#     'date':'2023-06-04 21:35:51',
#     'user_id':'5468686',
# }
    
# generate_deposit(data)
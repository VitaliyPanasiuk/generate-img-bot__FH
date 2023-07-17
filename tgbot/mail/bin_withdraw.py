from PIL import Image, ImageDraw, ImageFont
import textwrap

def split_text_by_width(text, max_width, font_size, font_path):
    image = Image.new("RGB", (1, 1))  # Создаем изображение размером 1x1 пиксель
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    lines = []
    current_line = ""
    l = text.split(" ")
    
    for word in l:
        word_width = draw.textsize(word, font=font)[0]
        
        if draw.textsize(current_line + "" + word, font=font)[0] <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
        print(current_line)
    
    lines.append(current_line.strip())
    
    return lines

def split_text_by_symbol_width(text, max_width, font_size, font_path):
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

def generate_bin_withdraw(data):
    deposit = Image.open('tgbot/mail/bin_withdraw_start.jpg')
    
    font = ImageFont.truetype('tgbot/mail/SFUIText-Semibold.ttf', size=23)
    draw_way = ImageDraw.Draw(deposit)
    draw_way.text(
		(52, 24),
		data['time'],
		font=font,
		fill='#22272a')
    
    # отрисовка суммы перевода
    font = ImageFont.truetype('tgbot/mail/aksans-regular.otf', size=30)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(217, 198),
    	data['date'],
    	font=font,
    	fill='#292929')
    
    font = ImageFont.truetype('tgbot/mail/aksans-050.otf', size=18)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(194, 330),
    	data['month'],
    	font=font,
    	fill='#575759')
    
    
    mess = f"Вы успешно вывели {data['amount']} {data['coin']} со своего счета."
    font = ImageFont.truetype('tgbot/mail/aksans-regular.otf', size=20)
    lines = split_text_by_width(mess,500,20,'tgbot/mail/aksans-regular.otf')
    
    start_y = 567
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (45, start_y),
            line,
            font=font,
            fill='#0e0e0e')
        
        start_y += 28
        
    font = ImageFont.truetype('tgbot/mail/aksans-regular.otf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(45, 683),
    	data['address'],
    	font=font,
    	fill='#0e0e0e')
        
    font = ImageFont.truetype('tgbot/mail/aksans-regular.otf', size=20)
    lines = split_text_by_symbol_width(data['tran_id'],380,20,'tgbot/mail/aksans-regular.otf')
    
    start_y = 743
    for line in lines:
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (45, start_y),
            line,
            font=font,
            fill='#0e0e0e')
        
        start_y += 28
    
    # deposit.show()
    deposit.save(f'tgbot/mail/{data["user_id"]}_output_bin_withdraw.png')
     

# data = {
#     'time': '14:07',
#     'date':'2023-06-19 12:38:40',
#     'month':'19 июня',
#     'amount':'210.00000000',
#     'coin':'USDT',
#     'address':'TTq4GUFGAh2a9VAzabsMfyaqZB8KTd9bim',
#     'tran_id':'9ece3c91c3d7a3889fe1afebd21fb4c2ce7200ecd28ed54f83971cbd3e5f037f',
#     'user_id':'5468686',
# }
    
# generate_deposit(data)
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

def generate_okx(data):
    deposit = Image.open('tgbot/mail/okx_start.jpg')
    
    font = ImageFont.truetype('tgbot/mail/SFUIText-Semibold.ttf', size=23)
    draw_way = ImageDraw.Draw(deposit)
    draw_way.text(
		(52, 24),
		data['time'],
		font=font,
		fill='#22272a')
    
    mess = f'Вы получили платеж в {data["currency"]}'
    font = ImageFont.truetype('tgbot/mail/aksans-regular.otf', size=30)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(25, 151),
    	mess,
    	font=font,
    	fill='#292929')
    
    font = ImageFont.truetype('tgbot/mail/aksans-500.otf', size=28)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(65, 480),
    	mess,
    	font=font,
    	fill='#292929')
    
    font = ImageFont.truetype('tgbot/mail/aksans-050.otf', size=18)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(160, 283),
    	data['month'],
    	font=font,
    	fill='#575759')
    
    mess = f"{data['amount']} {data['currency']}"
    font = ImageFont.truetype('tgbot/mail/aksans-500.otf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(65, 528),
    	mess,
    	font=font,
    	fill='#292929')
    
    mess2 = 'зачислено на ваш аккаунт в'
    mess = f"{data['amount']} {data['currency']}"
    font = ImageFont.truetype('tgbot/mail/aksans-250.otf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(65 + int(font.getsize(mess)[0]) + 8, 534),
    	mess2,
    	font=font,
    	fill='#292929')
    
    font = ImageFont.truetype('tgbot/mail/aksans-500.otf', size=20)
    draw_lev = ImageDraw.Draw(deposit)
    draw_lev.text(
    	(65, 560),
    	data['date'],
    	font=font,
    	fill='#292929')
    
        
    
    # deposit.show()
    deposit.save(f'tgbot/mail/{data["user_id"]}_output_okx.png')
    
     

# data = {
#     'time': '14:07',
#     'currency':'USDT',
#     'month':'14:25',
#     'amount':'21',
#     'date':'11.07.2023, 14:24:56',
#     'user_id':'5468686',
# }
    
# generate_okx(data)
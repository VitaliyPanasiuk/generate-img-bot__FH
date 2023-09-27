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

def generate_deposit_gistory(data):
    deposit = Image.open('tgbot/okx_history/deposit-start.png')
    
    font = ImageFont.truetype('tgbot/okx_history/SFUIText-Semibold.ttf', size=23)
    draw_way = ImageDraw.Draw(deposit)
    draw_way.text(
		(80, 26),
		data['time'],
		font=font,
		fill='#22272a')
    
    start_lab1 = 217
    start_lab2 = 240
    start_lab3 = 290
    start_time = 268
    start_line = 334
    start_sum = 247
    start_bal = 277
    for i in data['trans']:
    
        # отрисовка label
        font = ImageFont.truetype('tgbot/okx_history/aksans-regular.otf', size=20)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (21, start_lab1),
            'Внести средства',
            font=font,
            fill='#000000')
        
        font = ImageFont.truetype('tgbot/okx_history/aksans-regular.otf', size=20)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (21, start_lab2),
            'USDT',
            font=font,
            fill='#000000')
        
        font = ImageFont.truetype('tgbot/okx_history/aksans-regular.otf', size=16)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (21, start_lab3),
            'Депозит',
            font=font,
            fill='#939393')
        
        # отрисовка time tran
        font = ImageFont.truetype('tgbot/okx_history/aksans-regular.otf', size=16)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (21, start_time),
            i['time'],
            font=font,
            fill='#939393')
        
        # draw line after block
        line = Image.open('tgbot/okx_history/line.png')
        deposit.paste(line, (27, start_line))
        
        # draw sum and balance
        
        font = ImageFont.truetype('tgbot/okx_history/aksans-250.otf', size=20)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (566 - int(font.getsize('+')[0]) - int(font.getsize(i['sum'])[0]), start_sum),
            '+',
            font=font,
            fill='#4eb472')
        font = ImageFont.truetype('tgbot/okx_history/aksans-250.otf', size=20)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (566 - int(font.getsize(i['sum'])[0]), start_sum),
            i['sum'],
            font=font,
            fill='#4eb472')
        
        mes = 'Баланс ' + i['balance']
        font = ImageFont.truetype('tgbot/okx_history/aksans-regular.otf', size=16)
        draw_lev = ImageDraw.Draw(deposit)
        draw_lev.text(
            (566 - int(font.getsize(mes)[0]), start_bal),
            mes,
            font=font,
            fill='#939393')
        
        start_lab1 += 139
        start_lab2 += 139
        start_lab3 += 139
        start_time += 139
        start_line += 139
        start_sum += 139
        start_bal += 139
    
    
    
    # deposit.show()
    deposit.save(f'tgbot/okx_history/{data["user_id"]}_output.jpg')
     

# data = {
#     'time': '19:30',
#     'trans':[
#         {'time':'11.09.2023, 13:51:47',
#             'sum':'184,6461',
#             'balance':'184,6461',
#         },
#         {'time':'11.09.2023, 13:51:47',
#             'sum':'184,6461',
#             'balance':'184,6461',
#         },],
# }
    
# generate_bin_withdraw(data)
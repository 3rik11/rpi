import board
import busio
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template
import adafruit_ssd1306
import socket
import os
import time  # for animation timing

# Initialize I2C and OLED display (128x64)
i2c = busio.I2C(board.SCL, board.SDA)
device = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
app = Flask(__name__)

hidden = False  # global lock state

def get_pi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def clscreen():
    device.fill(0)
    device.show()

def display_url(ip):
    width = device.width
    height = device.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.isfile(font_path):
        font = ImageFont.truetype(font_path, 12)
    else:
        font = ImageFont.load_default()

    url_text = "URL:"
    ip_text = f"http://{ip}"

    bbox_url = font.getbbox(url_text)
    url_width = bbox_url[2] - bbox_url[0]

    bbox_ip = font.getbbox(ip_text)
    ip_width = bbox_ip[2] - bbox_ip[0]

    url_x = (width - url_width) // 2
    ip_x = (width - ip_width) // 2

    draw.text((url_x, 0), url_text, font=font, fill=255)
    draw.text((ip_x, 12), ip_text, font=font, fill=255)

    device.image(image)
    device.show()

def display_lock_prompt_with_url(ip):
    width = device.width
    height = device.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.isfile(font_path):
        font = ImageFont.truetype(font_path, 12)
    else:
        font = ImageFont.load_default()

    # Draw URL at top
    url_text = "URL:"
    ip_text = f"http://{ip}"

    bbox_url = font.getbbox(url_text)
    url_width = bbox_url[2] - bbox_url[0]
    bbox_ip = font.getbbox(ip_text)
    ip_width = bbox_ip[2] - bbox_ip[0]

    url_x = (width - url_width) // 2
    ip_x = (width - ip_width) // 2

    draw.text((url_x, 0), url_text, font=font, fill=255)
    draw.text((ip_x, 12), ip_text, font=font, fill=255)

    # Draw lock prompt at bottom, moved one line up
    lock_emoji = "[0]"
    prompt_text = "can you unlock it?"

    bbox_lock = font.getbbox(lock_emoji)
    lock_width = bbox_lock[2] - bbox_lock[0]
    lock_height = bbox_lock[3] - bbox_lock[1]

    bbox_prompt = font.getbbox(prompt_text)
    prompt_width = bbox_prompt[2] - bbox_prompt[0]

    lock_x = (width - lock_width) // 2  # Centered horizontally
    lock_y = height - lock_height - 24  # moved one line up (12 pixels)

    draw.text((lock_x, lock_y), lock_emoji, font=font, fill=255)

    device.image(image)
    device.show()

def display_unlock_animation():
    global hidden
    width = device.width
    height = device.height

    clscreen()

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.isfile(font_path):
        font_small = ImageFont.truetype(font_path, 14)
        font_smaller = ImageFont.truetype(font_path, 12)
    else:
        font_small = ImageFont.load_default()
        font_smaller = ImageFont.load_default()

    unlocking_y = 10

    bar_x0, bar_y0 = 16, height // 2
    bar_x1, bar_y1 = width - 16, height // 2 + 12
    bar_width = bar_x1 - bar_x0

    for i in range(bar_width + 1):
        image = Image.new("1", (width, height))
        draw = ImageDraw.Draw(image)

        message = "UNLOCKING..."
        bbox_msg = font_small.getbbox(message)
        msg_x = (width - (bbox_msg[2] - bbox_msg[0])) // 2
        draw.text((msg_x, unlocking_y), message, font=font_small, fill=255)

        draw.rectangle([bar_x0, bar_y0, bar_x1, bar_y1], outline=255, fill=0)
        if i > 0:
            draw.rectangle([bar_x0, bar_y0, bar_x0 + i, bar_y1], outline=255, fill=255)

        device.image(image)
        device.show()
        time.sleep(0.02)

    sparkle_positions = [
        (width // 4, height // 4),
        (3 * width // 4, height // 4),
        (width // 4, 3 * height // 4),
        (3 * width // 4, 3 * height // 4),
        (width // 2, height // 2)
    ]

    for _ in range(3):
        for pos in sparkle_positions:
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)

            access_text = "ACCESS"
            bbox_access = font_smaller.getbbox(access_text)
            access_x = (width - (bbox_access[2] - bbox_access[0])) // 2
            access_y = 10

            granted_text = "GRANTED"
            bbox_granted = font_smaller.getbbox(granted_text)
            granted_x = (width - (bbox_granted[2] - bbox_granted[0])) // 2
            granted_y = access_y + (bbox_access[3] - bbox_access[1]) + 5

            draw.text((access_x, access_y), access_text, font=font_smaller, fill=255)
            draw.text((granted_x, granted_y), granted_text, font=font_smaller, fill=255)

            for (x, y) in sparkle_positions:
                draw.line((x - 2, y, x + 2, y), fill=255)
                draw.line((x, y - 2, x, y + 2), fill=255)

            device.image(image)
            device.show()
            time.sleep(0.3)

            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)
            draw.text((access_x, access_y), access_text, font=font_smaller, fill=255)
            draw.text((granted_x, granted_y), granted_text, font=font_smaller, fill=255)
            device.image(image)
            device.show()
            time.sleep(0.15)

    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((access_x, access_y), access_text, font=font_smaller, fill=255)
    draw.text((granted_x, granted_y), granted_text, font=font_smaller, fill=255)
    device.image(image)
    device.show()

    hidden = True


@app.route('/')
def index():
    global hidden
    clscreen()
    pi_ip = get_pi_ip()
    if hidden:
        display_url(pi_ip)
    else:
        display_lock_prompt_with_url(pi_ip)
    return render_template("index.html", ip=pi_ip)

@app.route('/hidden')
def unlock():
    global hidden
    clscreen()
    display_unlock_animation()
    time.sleep(1)
    pi_ip = get_pi_ip()
    display_url(pi_ip)
    return "<h1>Lock unlocked. Enjoy the animation!</h1>"

if __name__ == '__main__':
    pi_ip = get_pi_ip()
    clscreen()
    display_lock_prompt_with_url(pi_ip)
    app.run(host='0.0.0.0', port=5000)

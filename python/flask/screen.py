
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Initialize I2C and OLED display (128x64)
i2c = busio.I2C(board.SCL, board.SDA)
device = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Your website API endpoint that returns number of users
def text(message, position):
    # Clear display
    device.fill(0)
    device.show()

    # Create blank image for drawing.
    width = device.width
    height = device.height
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Load default font.
    font = ImageFont.load_default()

    # Draw text
    draw.text(position, message, font=font, fill=255)

    # Display image
    device.image(image)
    device.show()
    
    
text("Hi", (0, 0))

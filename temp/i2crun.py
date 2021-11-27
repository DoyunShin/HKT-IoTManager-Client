import I2C
from time import *

lcd = I2C.lcd()
lcd.lcd_display_string("2021/11/27", 1)
lcd.lcd_display_string("Temperature:6C", 2)
#lcd.lcd_clear()
#lcd.lcd_display_string("2021/11/27", 1)
#lcd.lcd_display_string("Temperature:21C", 2)


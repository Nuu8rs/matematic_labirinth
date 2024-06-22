width = 20
height = 20
border = 5
width_line = 40
width_walls = 5
info_height = 70
color_way = (255, 255, 255)
color_wall = (0, 0, 0)
color_player = (0, 0, 255)
color_start = (0, 255, 0)
color_finish = (255, 0, 0)

class SettingsDisplay:
    
    @property
    def width_window(self):
        return ((width * 2 - 1) // 2 + 1) * width_line + ((width * 2 - 1) // 2) * width_walls + border * 2

    @property
    def height_window(self):
        return ((height * 2 - 1) // 2 + 1) * width_line + ((height * 2 - 1) // 2) * width_walls + border * 2 + info_height

    
display = SettingsDisplay()
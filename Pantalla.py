from screeninfo import get_monitors

class Pantalla:
    def __init__(self, width, height):
        self.Monitor = get_monitors()[1]
        self.Screen_width = self.Monitor.width
        self.Screen_height = self.Monitor.height
        self.X_Pos = self.Get_X(width)
        self.Y_Pos = self.Get_Y(height)
    
    def Get_X(self, width):
        return (self.Screen_width - width) // 2
    
    def Get_Y(self, height):
        return (self.Screen_height - height) // 2
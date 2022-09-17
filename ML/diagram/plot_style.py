import matplotlib.pyplot as plt

class plot_style:
    def __init__(self):
        self.background = "grayscale"
        self.node_size = 100
        self.font_size = 8

    def select(self, style):
        self.style = style
        if self.style == "white":
            self.background = 'seaborn-bright'
            self.node_size = 135
            self.font_size = 8

        elif self.style == "gray":
            self.background = 'classic'
            self.node_size = 200
            self.font_size = 10

        elif self.style == "black":
            self.background = 'dark_background'
            self.node_size = 135
            self.font_size = 8
        
    def _print_style():
        # Print available plot styles (background color)
        for style in plt.style.available:
            print(style)
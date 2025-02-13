import matplotlib.pyplot as plt

import flet as ft
from Chart import Chart
import os

class DonutChart(Chart):
    def __init__(self, title, values, fontSize, colors):
        super().__init__(title)
        self.values = values
        self.fontSize = fontSize
        self.colors = colors
        # self.fontSizeForTitle = fontSizeForTitle

    def save(self, image_path):
        fig, ax = plt.subplots()
        ax.pie(
            self.values,
            startangle=90,
            counterclock=False,

            wedgeprops=dict(width=0.2, linewidth=1),

            colors = self.colors
        )
        ax.axis('equal')


        ax.text(0, 0, f'{round(self.values[0])}%', ha='center', va='center', fontsize=self.fontSize, color='white', weight='bold')
        # fig.text(0.5, 0.01, self.title, ha='center', va='center', fontsize = 30,  color='white', weight='bold')

        self.save_image(fig, image_path)

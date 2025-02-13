import  flet
import os
import matplotlib.pyplot as plt

class Chart:
    def __init__(self, title):
        self.title = title

    def save_image(self, fig, image_path):
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path, transparent=True)
        plt.close(fig)
        print(f"Image saved: {image_path}")
from settings import *
from PIL import Image, ImageTk
import json


def load():
    with open("details.json", "r", encoding="utf8") as f:
        return json.load(f)
    
def save(info):
    with open("details.json", "w", encoding="utf8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    
def width_percentage(percentage):
    return (SCREEN_WIDTH / 100) * percentage
    
def height_percentage(percentage):
    return (SCREEN_HEIGHT / 100) * percentage

def get_image(path):
    return ImageTk.PhotoImage(Image.open(path).resize((BLOCK_WIDTH, BLOCK_HEIGHT)))  

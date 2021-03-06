import os
from tkinter import END
from PIL.ImageTk import PhotoImage
from Script.Core import cache_contorl, game_path_config, main_frame

game_path = game_path_config.game_path
textbox = main_frame.textbox
image_data = {}
image_text_data = {}
image_lock = 0


def get_image_data(image_name: str, image_path="") -> PhotoImage:
    """
    按路径读取图片数据并创建PhotoImage对象
    Keyword arguments:
    image_name -- 图片名字
    image_path -- 图片路径 (default '')
    """
    if image_path == "":
        image_path = os.path.join(game_path, "image", image_name + ".png")
    else:
        image_path = os.path.join(
            game_path, "image", image_path, image_name + ".png"
        )
    cache_contorl.image_id += 1
    return PhotoImage(file=image_path)


def print_image(image_name: str, image_path=""):
    """
    绘制图片的内部实现，按图片id将图片加入绘制队列
    Keyword arguments:
    image_name -- 图片名字
    image_path -- 图片路径 (default '')
    """
    image_data[str(cache_contorl.image_id)] = get_image_data(
        image_name, image_path
    )
    textbox.image_create(END, image=image_data[str(cache_contorl.image_id)])

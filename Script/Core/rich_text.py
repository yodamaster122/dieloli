from Script.Core import (
    game_config,
    cache_contorl,
    text_loading,
    dictionaries,
    constant,
)


def set_rich_text_print(text_message: str, default_style: str) -> list:
    """
    获取文本的富文本样式列表
    Keyword arguments:
    text_message -- 原始文本
    default_style -- 无富文本样式时的默认样式
    """
    style_name_list = {
        key: 0
        for key in game_config.get_font_data_list()
        + list(
            text_loading.get_game_data(
                constant.FilePath.BAR_CONFIG_PATH
            ).keys()
        )
    }
    style_index = 0
    style_last_index = None
    style_max_index = None
    style_list = []
    for key in style_name_list:
        style_text_head = "<" + key + ">"
        if style_text_head in text_message:
            style_index = 1
    if style_index == 0:
        style_list = [default_style] * len(text_message)
    else:
        for i in range(0, len(text_message)):
            input_text_style_size = text_message.find(">", i) + 1
            input_text_style = text_message[i + 1 : input_text_style_size - 1]
            if text_message[i] == "<" and (
                (input_text_style in style_name_list)
                or (input_text_style[1:] in style_name_list)
            ):
                style_last_index = i
                style_max_index = input_text_style_size
                if input_text_style[0] == "/":
                    if cache_contorl.text_style_position["position"] == 1:
                        cache_contorl.output_text_style = "standard"
                        cache_contorl.text_style_position["position"] = 0
                        cache_contorl.text_style_cache = ["standard"]
                    else:
                        cache_contorl.text_style_position["position"] = (
                            cache_contorl.text_style_position["position"] - 1
                        )
                        cache_contorl.output_text_style = cache_contorl.text_style_cache[
                            cache_contorl.text_style_position["position"]
                        ]
                else:
                    cache_contorl.text_style_position["position"] = len(
                        cache_contorl.text_style_cache
                    )
                    cache_contorl.text_style_cache.append(input_text_style)
                    cache_contorl.output_text_style = cache_contorl.text_style_cache[
                        cache_contorl.text_style_position["position"]
                    ]
            else:
                if style_last_index is not None:
                    if i == len(text_message):
                        cache_contorl.text_style_position["position"] = 0
                        cache_contorl.output_text_style = "standard"
                        cache_contorl.text_style_cache = ["standard"]
                    if i not in range(style_last_index, style_max_index):
                        style_list.append(cache_contorl.output_text_style)
                else:
                    style_list.append(cache_contorl.output_text_style)
    return style_list


def remove_rich_cache(string: str) -> str:
    """
    移除文本中的富文本标签
    Keyword arguments:
    string -- 原始文本
    """
    string = dictionaries.handle_text(string)
    bar_list = list(
        text_loading.get_game_data(constant.FilePath.BAR_CONFIG_PATH).keys()
    )
    style_name_list = game_config.get_font_data_list() + bar_list
    for i in range(0, len(style_name_list)):
        style_text_head = "<" + style_name_list[i] + ">"
        style_text_tail = "</" + style_name_list[i] + ">"
        if style_text_head in string:
            string = string.replace(style_text_head, "")
            string = string.replace(style_text_tail, "")
    return string

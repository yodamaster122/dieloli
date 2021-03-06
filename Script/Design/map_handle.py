import os
import time
from Script.Core import (
    era_print,
    py_cmd,
    cache_contorl,
    value_handle,
    text_handle,
)


def print_map(map_path: list) -> list:
    """
    按地图路径绘制地图
    Ketword arguments:
    map_path -- 地图路径
    """
    map_path_str = get_map_system_path_str_for_list(map_path)
    map_draw = get_map_draw_for_map_path(map_path_str)
    character_position = cache_contorl.character_data["character"][0].position
    character_now_scene_id = get_scene_id_in_map_for_scene_path_on_map_path(
        character_position, map_path
    )
    input_s = []
    map_y_list = map_draw["Draw"]
    map_x_cmd_list_data = map_draw["Cmd"]
    map_x_cmd_id_list_data = map_draw["CmdId"]
    for map_x_list_id in range(len(map_y_list)):
        map_x_list = map_y_list[map_x_list_id]
        now_cmd_list = map_x_cmd_list_data[map_x_list_id]
        now_cmd_id_list = map_x_cmd_id_list_data[map_x_list_id]
        cmd_list_str = "".join(now_cmd_list)
        era_print.normal_print(
            text_handle.align(map_x_list + cmd_list_str, "center", True),
            rich_text_judge=False,
        )
        i = 0
        while i in range(len(map_x_list)):
            if now_cmd_id_list != []:
                while i == now_cmd_id_list[0]:
                    if now_cmd_list[0] == character_now_scene_id:
                        era_print.normal_print(
                            now_cmd_list[0], "nowmap", rich_text_judge=False
                        )
                        input_s.append(None)
                    else:
                        py_cmd.pcmd(now_cmd_list[0], now_cmd_list[0], None)
                        input_s.append(now_cmd_list[0])
                    now_cmd_list = now_cmd_list[1:]
                    now_cmd_id_list = now_cmd_id_list[1:]
                    if now_cmd_list == []:
                        break
                if now_cmd_id_list != []:
                    era_print.normal_print(map_x_list[i : now_cmd_id_list[0]])
                    i = now_cmd_id_list[0]
                else:
                    era_print.normal_print(map_x_list[i:])
                    i = len(map_x_list)
            else:
                era_print.normal_print(map_x_list[i:])
                i = len(map_x_list)
        era_print.line_feed_print()
    return input_s


def get_map_draw_for_map_path(map_path_str: str) -> str:
    """
    从地图路径获取地图绘制数据
    Keyword arguments:
    map_path -- 地图路径
    """
    map_data = get_map_data_for_map_path(map_path_str)
    return map_data["MapDraw"]


def get_scene_id_in_map_for_scene_path_on_map_path(
    scene_path: list, map_path: list
) -> list:
    """
    获取场景在地图上的相对位置
    Keyword arguments:
    scene_path -- 场景路径
    map_path -- 地图路径
    """
    return scene_path[len(map_path)]


def get_map_for_path(scene_path: list) -> list:
    """
    查找场景所在地图路径
    Keyword arguments:
    scene_path -- 场景路径
    """
    map_path = scene_path[:-1]
    map_path_str = get_map_system_path_str_for_list(map_path)
    if map_path_str in cache_contorl.map_data:
        return map_path
    return get_map_for_path(map_path)


def get_map_data_for_map_path(map_path_str: str) -> dict:
    """
    从地图路径获取地图数据
    Keyword arguments:
    map_path -- 地图路径
    """
    return cache_contorl.map_data[map_path_str].copy()


def get_scene_list_for_map(map_path_str: str) -> list:
    """
    获取地图下所有场景
    Keyword arguments:
    map_path -- 地图路径
    """
    map_data = get_map_data_for_map_path(map_path_str)
    scene_list = list(map_data["PathEdge"].keys())
    return scene_list


def get_scene_name_list_for_map_path(map_path_str: str):
    """
    获取地图下所有场景的名字
    Keyword arguments:
    map_path -- 地图路径
    """
    scene_list = get_scene_list_for_map(map_path_str)
    scene_name_data = {}
    for scene in scene_list:
        load_scene_data = get_scene_data_for_map(map_path_str, scene)
        scene_name = load_scene_data["SceneName"]
        scene_name_data[scene] = scene_name
    return scene_name_data


def character_move_scene(
    old_scene_path: list, new_scene_path: list, character_id: int
):
    """
    将角色移动至新场景
    Keyword arguments:
    old_scene_path -- 旧场景路径
    new_scene_path -- 新场景路径
    character_id -- 角色id
    """
    old_scene_path_str = get_map_system_path_str_for_list(old_scene_path)
    new_scene_path_str = get_map_system_path_str_for_list(new_scene_path)
    if (
        character_id
        in cache_contorl.scene_data[old_scene_path_str]["SceneCharacterData"]
    ):
        del cache_contorl.scene_data[old_scene_path_str]["SceneCharacterData"][
            character_id
        ]
    if (
        character_id
        not in cache_contorl.scene_data[new_scene_path_str][
            "SceneCharacterData"
        ]
    ):
        cache_contorl.character_data["character"][
            character_id
        ].position = new_scene_path
        cache_contorl.scene_data[new_scene_path_str]["SceneCharacterData"][
            character_id
        ] = 0


def get_map_system_path_str_for_list(now_list: list):
    """
    将地图路径列表数据转换为字符串
    Keyword arguments:
    now_list -- 地图路径列表数据
    """
    return os.sep.join(now_list)


def get_path_finding(
    map_path_str: str, now_node: str, target_node: str
) -> (str, list):
    """
    查询寻路路径
    Keyword arguments:
    map_path -- 地图路径
    now_node -- 当前节点相对位置
    target_node -- 目标节点相对位置
    Return arguments:
    str:end -- 寻路路径终点
    lisr -- 寻路路径
    """
    if now_node == target_node:
        return "End", []
    else:
        return (
            "",
            cache_contorl.map_data[map_path_str]["SortedPath"][now_node][
                target_node
            ],
        )


def get_scene_to_scene_map_list(
    now_scene_path: list, target_scene_path: list
) -> (str, list):
    """
    获取场景到场景之间需要经过的地图列表
    如果两个场景属于同一地图并在同一层级，则返回common
    Keyword arguments:
    now_scene_path -- 当前场景路径
    target_scene_path -- 目标场景路径
    Return arguments:
    str:common -- 两个场景在同一层级
    list -- 场景层级路径列表
    """
    scene_affiliation = judge_scene_affiliation(
        now_scene_path, target_scene_path
    )
    if scene_affiliation == "common":
        return "common", []
    elif scene_affiliation == "subordinate":
        return (
            "",
            get_map_hierarchy_list_for_scene_path(
                now_scene_path, target_scene_path
            ),
        )
    elif scene_affiliation == "nobelonged":
        common_map = get_common_map_for_scene_path(
            now_scene_path, target_scene_path
        )
        now_scene_to_common_map = get_map_hierarchy_list_for_scene_path(
            now_scene_path, common_map
        )
        target_scene_to_common_map = get_map_hierarchy_list_for_scene_path(
            target_scene_path, common_map
        )
        common_map_to_target_scene = value_handle.reverse_array_list(
            target_scene_to_common_map
        )
        return "", now_scene_to_common_map + common_map_to_target_scene[1:]


def get_common_map_for_scene_path(
    scene_a_path: list, scene_b_path: list
) -> list:
    """
    查找场景共同所属地图
    Keyword arguments:
    scene_aPath -- 场景A路径
    scene_bpath -- 场景B路径
    """
    hierarchy = []
    if scene_a_path[:-1] == [] or scene_b_path[:-1] == []:
        return hierarchy
    else:
        for i in range(0, len(scene_a_path)):
            try:
                if scene_a_path[i] == scene_b_path[i]:
                    hierarchy.append(scene_a_path[i])
                else:
                    break
            except IndexError:
                break
        return get_map_path_for_true(hierarchy)


def get_map_hierarchy_list_for_scene_path(
    now_scene_path: list, target_scene_path: list
) -> list:
    """
    查找当前场景到目标场景之间的层级列表(仅当当前场景属于目标场景的子场景时可用)
    Keyword arguments:
    now_scene_path -- 当前场景路径
    target_scene_path -- 目标场景路径
    Return arguments:
    hierarchy_list -- 当前场景路径到目标场景路径之间的层级列表
    """
    hierarchy_list = []
    now_path = None
    while True:
        if now_path is None:
            now_path = now_scene_path[:-1]
        if now_path != target_scene_path:
            hierarchy_list.append(now_path)
            now_path = now_path[:-1]
        else:
            break
    return hierarchy_list


def get_map_path_for_true(map_path: list) -> list:
    """
    判断地图路径是否是有效的地图路径，若不是，则查找上层路径，直到找到有效地图路径并返回
    Keyword arguments:
    map_path -- 当前地图路径
    """
    map_path_str = get_map_system_path_str_for_list(map_path)
    if map_path_str in cache_contorl.map_data:
        return map_path
    else:
        new_map_path = map_path[:-1]
        return get_map_path_for_true(new_map_path)


def judge_scene_is_affiliation(
    now_scene_path: list, target_scene_path: list
) -> str:
    """
    获取场景所属关系
    当前场景属于目标场景的子场景 -> 返回'subordinate'
    目标场景属于当前场景的子场景 -> 返回'superior'
    other -> 返回'common'
    Keyword arguments:
    now_scene_path -- 当前场景路径
    target_scene_path -- 目标场景路径
    """
    if (
        judge_scene_affiliation(now_scene_path, target_scene_path)
        == "subordinate"
    ):
        return "subordinate"
    elif (
        judge_scene_affiliation(target_scene_path, now_scene_path)
        == "subordinate"
    ):
        return "superior"
    return "common"


def judge_scene_affiliation(
    now_scene_path: list, target_scene_path: list
) -> str:
    """
    判断场景有无所属关系
    当前场景属于目标场景的子场景 -> 返回'subordinate'
    当前场景与目标场景的第一个上级场景相同 -> 返回'common'
    other -> 返回'nobelonged'
    Keyword arguments:
    now_scene_path -- 当前场景路径
    target_scene_path -- 目标场景路径
    """
    if now_scene_path[:-1] != target_scene_path[:-1]:
        if now_scene_path[:-1] != target_scene_path:
            if now_scene_path[:-1] != []:
                return judge_scene_affiliation(
                    now_scene_path[:-1], target_scene_path
                )
            else:
                return "nobelonged"
        else:
            return "subordinate"
    return "common"


def get_relation_map_list_for_scene_path(scene_path: list) -> list:
    """
    获取场景所在所有直接地图(当前场景id为0，所在地图在上层地图相对位置也为0，视为直接地图)位置
    Keyword arguments:
    scene_path -- 当前场景路径
    """
    now_path = scene_path
    now_map_path = scene_path[:-1]
    now_pathId = now_path[-1]
    map_list = []
    if now_map_path != [] and now_map_path[:-1] != []:
        map_list.append(now_map_path)
        if now_pathId == "0":
            return map_list + get_relation_map_list_for_scene_path(
                now_map_path
            )
        else:
            return map_list
    else:
        map_list.append(now_map_path)
        return map_list


def get_scene_data_for_map(map_path_str: str, map_scene_id: str) -> dict:
    """
    载入地图下对应场景数据
    Keyword arguments:
    map_path -- 地图路径
    map_scene_id -- 场景相对位置
    """
    if map_path_str == "":
        scene_path_str = map_scene_id
    else:
        scene_path_str = map_path_str + os.sep + str(map_scene_id)
    scene_path = get_map_system_path_for_str(scene_path_str)
    scene_path = get_scene_path_for_true(scene_path)
    scene_path_str = get_map_system_path_str_for_list(scene_path)
    return cache_contorl.scene_data[scene_path_str]


def get_scene_path_for_map_scene_id(map_path: list, map_scene_id: str) -> list:
    """
    从场景在地图中的相对位置获取场景路径
    Keyword arguments:
    map_path -- 地图路径
    map_scene_id -- 场景在地图中的相对位置
    """
    new_scene_path = map_path.copy()
    new_scene_path.append(map_scene_id)
    new_scene_path = get_scene_path_for_true(new_scene_path)
    return new_scene_path


def get_map_system_path_for_str(path_str: str) -> list:
    """
    将地图系统路径文本转换为地图系统路径
    """
    return path_str.split(os.sep)


def get_map_scene_id_for_scene_path(map_path: list, scene_path: list) -> str:
    """
    从场景路径查找场景在地图中的相对位置
    Keyword arguments:
    map_path -- 地图路径
    scene_path -- 场景路径
    """
    return scene_path[len(map_path)]


def get_scene_path_for_true(scene_path: list) -> list:
    """
    获取场景的有效路径(当前路径下若不存在场景数据，则获取当前路径下相对位置为0的路径)
    Keyword arguments:
    scene_path -- 场景路径
    """
    scene_path_str = get_map_system_path_str_for_list(scene_path)
    if scene_path_str in cache_contorl.scene_data:
        return scene_path
    else:
        scene_path.append("0")
        return get_scene_path_for_true(scene_path)


def get_map_door_data_for_scene_path(scene_path: list) -> dict:
    """
    从场景路径获取当前地图到其他地图的门数据
    Keyword arguments:
    scene_path -- 场景路径
    """
    map_path = get_map_for_path(scene_path)
    map_path_str = get_map_system_path_str_for_list(map_path)
    return get_map_door_data(map_path_str)


def get_map_door_data(map_path_str: str) -> dict:
    """
    获取地图下通往其他地图的门数据
    Keyword arguments:
    map_path -- 地图路径
    """
    map_data = cache_contorl.map_data[map_path_str]
    if "MapDoor" in map_data:
        return map_data["MapDoor"]
    else:
        return {}


def get_scene_character_name_list(
    scene_path_str: str, remove_own_character=False
) -> list:
    """
    获取场景上所有角色的姓名列表
    Keyword arguments:
    scene_path -- 场景路径
    remove_own_character -- 从姓名列表中移除主角 (default False)
    """
    scene_character_data = cache_contorl.scene_data[scene_path_str][
        "SceneCharacterData"
    ]
    now_scene_character_list = list(scene_character_data.keys())
    name_list = []
    if remove_own_character:
        now_scene_character_list.remove(0)
    for character_id in now_scene_character_list:
        character_name = cache_contorl.character_data["character"][
            character_id
        ].name
        name_list.append(character_name)
    return name_list


def get_character_id_by_character_name(
    character_name: str, scene_path_str: str
) -> str:
    """
    获取场景上角色姓名对应的角色id
    Keyword arguments:
    character_name -- 角色姓名
    scene_path -- 场景路径
    """
    character_nameList = get_scene_character_name_list(scene_path_str)
    character_nameIndex = character_nameList.index(character_name)
    character_idList = get_scene_character_id_list(scene_path_str)
    return character_idList[character_nameIndex]


def get_scene_character_id_list(scene_path_str: str) -> list:
    """
    获取场景上所有角色的id列表
    Keyword arguments:
    scene_path -- 场景路径
    """
    return list(
        cache_contorl.scene_data[scene_path_str]["SceneCharacterData"].keys()
    )


def sort_scene_character_id(scene_path_str: str):
    """
    对场景上的角色按好感度进行排序
    Keyword arguments:
    scene_path -- 场景路径
    """
    now_scene_character_intimate_data = {}
    for character in cache_contorl.scene_data[scene_path_str][
        "SceneCharacterData"
    ]:
        now_scene_character_intimate_data[
            character
        ] = cache_contorl.character_data["character"][character].intimate
    new_scene_character_intimate_data = sorted(
        now_scene_character_intimate_data.items(),
        key=lambda x: (x[1], -int(x[0])),
        reverse=True,
    )
    new_scene_character_intimate_data = value_handle.two_bit_array_to_dict(
        new_scene_character_intimate_data
    )
    cache_contorl.scene_data[scene_path_str][
        "SceneCharacterData"
    ] = new_scene_character_intimate_data

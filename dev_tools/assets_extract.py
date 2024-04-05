# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import json
import numpy as np

from tqdm.contrib.concurrent import process_map
from pathlib import Path

from module.logger import logger

MODULE_FOLDER = 'tasks'
ASSETS_FILE = 'assets.py'
ASSETS_CLASS = '\nclass Assets: \n'
IMPORT_EXP = """
from module.atom.image import RuleImage
from module.atom.click import RuleClick
from module.atom.long_click import RuleLongClick
from module.atom.swipe import RuleSwipe
from module.atom.ocr import RuleOcr
from module.atom.list import RuleList

# This file was automatically generated by ./dev_tools/assets_extract.py.
# Don't modify it manually.
"""
IMPORT_EXP = IMPORT_EXP.strip().split('MODULE_FOLDER') + ['']


def name_transform(name: str) -> str:
    """
    转换名称, 把小写的转化为大写的, 带有数字的不变，有下划线继续有下划线,
    如果是全部的大写就不管
    :param name: 任务名
    :return: 转换后的名称
    """
    if name.isupper():
        return name
    if name.islower():
        return name.upper()
    return name.upper()


class ImageExtractor:

    def __init__(self, file: str, data: list) -> None:
        """
        image rule 提取
        :param data:  json解析后的数据
        """
        # 这个时候的路径分隔符变成了 /
        self.file = str(Path(file).resolve().relative_to((Path.cwd()).resolve()).as_posix())
        self.image_path = Path(self.file).parent.as_posix()

        self._result = '\n\n\t# Image Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tI_{name_transform(item["itemName"])} = RuleImage(' \
                    f'roi_front=({item["roiFront"]}), ' \
                    f'roi_back=({item["roiBack"]}), ' \
                    f'threshold={item["threshold"]}, ' \
                    f'method="{item["method"]}", ' \
                    f'file="./{self.image_path}/{item["imageName"]}")\n'
        return description + name


class ClickExtractor:

    def __init__(self, file: str, data: list) -> None:
        """
        click rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Click Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tC_{name_transform(item["itemName"])} = RuleClick(' \
                    f'roi_front=({item["roiFront"]}), ' \
                    f'roi_back=({item["roiBack"]}), ' \
                    f'name="{item["itemName"]}")\n'
        return description + name


class LongClickExtractor:

    def __init__(self, file: str, data: list) -> None:
        """
        long click rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Long Click Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tL_{name_transform(item["itemName"])} = RuleLongClick(' \
                    f'roi_front=({item["roiFront"]}), ' \
                    f'roi_back=({item["roiBack"]}), ' \
                    f'duration={item["duration"]}, ' \
                    f'name="{item["itemName"]}")\n'
        return description + name


class SwipeExtractor:

    def __init__(self, file: str, data: list) -> None:
        """
        swipe rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Swipe Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tS_{name_transform(item["itemName"])} = RuleSwipe(' \
                    f'roi_front=({item["roiFront"]}), ' \
                    f'roi_back=({item["roiBack"]}), ' \
                    f'mode="{item["mode"]}", ' \
                    f'name="{item["itemName"]}")\n'
        return description + name


class OcrExtractor:
    def __init__(self, file: str, data: list) -> None:
        """
        swipe rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Ocr Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    @classmethod
    def extract_item(cls, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tO_{name_transform(item["itemName"])} = RuleOcr(' \
                    f'roi=({item["roiFront"]}), ' \
                    f'area=({item["roiBack"]}), ' \
                    f'mode="{item["mode"]}", ' \
                    f'method="{item["method"]}", ' \
                    f'keyword="{item["keyword"]}", ' \
                    f'name="{item["itemName"]}")\n'
        return description + name


class ListExtractor:
    def __init__(self, file: str, data: dict) -> None:
        """
        List rule 提取
        :param data:  json解析后的数据
        """
        self.file = str(Path(file).resolve().relative_to((Path.cwd()).resolve()).as_posix())
        self.image_path = Path(self.file).parent.as_posix()
        self._result = '\n\n\t# List Rule Assets\n'

        if not isinstance(data, dict):
            raise TypeError("data must be dict")

        self._result += self.extract(data)

    @property
    def result(self) -> str:
        return self._result

    def extract(self, data) -> str:
        """
        解析每一项，返回字符串
        :param data:
        :return:
        """
        width, height = 0, 0
        array: list = []
        for item in data["list"]:
            roi_front = item["roiFront"].split(",")
            width += int(roi_front[2])
            height += int(roi_front[3])
            array.append(f'"{item["itemName"]}"')
        width = int(width / len(data["list"]))
        height = int(height / len(data["list"]))
        array = ', '.join(array)

        description: str = f'\t# {data["description"]} \n'
        name: str = f'\tL_{name_transform(data["name"])} = RuleList(' \
                    f'folder="./{str(self.image_path)}", ' \
                    f'direction="{data["direction"]}", ' \
                    f'mode="{data["type"]}", ' \
                    f'roi_back=({data["roiBack"]}), ' \
                    f'size=({width}, {height}), ' \
                    f'\n\t\t\t\t\t array=[{str(array)}])\n'
        return description + name


class AssetsExtractor:

    def __init__(self, task_path: str) -> None:
        """
        assets 提取某个任务文件夹下的所以的资源
        :param task_name: 任务名
        """

        self.task_path = Path(task_path)
        self.task_name = self.task_path.name
        self.assets_file = self.task_path / ASSETS_FILE

        self.class_name = f'\nclass {self.task_name}Assets: \n'

        self._result = ''
        for import_exp in IMPORT_EXP:
            self._result += import_exp
        self._result += self.class_name

    def all_json_file(self) -> list:
        """
        获取所有json文件
        :return: json文件（带后缀）列表
        """
        return [str(x) for x in self.task_path.rglob('*.json') if 'temp' not in str(x)]

    @classmethod
    def read_file(cls, file: str) -> list:
        """
        读文件并随带解析
        :param file:
        :return:
        """
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list) and not isinstance(data, dict):
            logger.error(f'{file} 文件解析错误，不是list 或者 dict')
            return None
        return data

    @classmethod
    def is_image_file(cls, data: list) -> bool:
        """
        判断是不是imagerule 文件
        :param data: 解析后的json数据，是list
        :return:
        """
        item = data[0]
        if 'imageName' in item:
            return True
        return False

    @classmethod
    def is_click_file(cls, data: list) -> bool:
        """
        判断是不是clickrule 文件, 我这样的判断是有点不合规的
        :param data: 解析后的json数据，是list
        :return:
        """
        item = data[0]
        return len(item) == 4

    @classmethod
    def is_long_click_file(cls, data: list) -> bool:
        """
        判断是不是longclickrule 文件
        :param data: 解析后的json数据，是list
        :return:
        """
        item = data[0]
        if 'duration' in item:
            return True
        return False

    @classmethod
    def is_swipe_file(cls, data: list) -> bool:
        """
        判断是不是swipe rule 文件
        :param data: 解析后的json数据，是list
        :return:
        """
        item = data[0]
        if 'mode' in item and len(item) == 5:
            return True
        return False

    @classmethod
    def is_ocr_file(cls, data: list) -> bool:
        """
        判断是不是ocr 文件
        :param data: 解析后的json数据，是list
        :return:
        """
        item = data[0]
        if 'keyword' in item:
            return True
        return False

    @classmethod
    def is_list_file(cls, data) -> bool:
        """

        :param data:
        :return:
        """
        if isinstance(data, dict) and 'name' in data:
            return True
        return False

    def write_file(self) -> None:
        """
        将自身的_resule写入文件
        :return:
        """
        with open(self.assets_file, 'w', encoding='utf-8') as f:
            f.write(self._result)

    def extract(self) -> str:
        """
        生成一个assets.py文件
        :return:
        """
        result = ''
        for file in self.all_json_file():
            data = self.read_file(file)
            if not data:
                continue

            if self.is_list_file(data):
                result += ListExtractor(file, data).result
                continue
            if self.is_image_file(data):
                result += ImageExtractor(file, data).result
            elif self.is_click_file(data):
                result += ClickExtractor(file, data).result
            elif self.is_long_click_file(data):
                result += LongClickExtractor(file, data).result
            elif self.is_swipe_file(data):
                result += SwipeExtractor(file, data).result
            elif self.is_ocr_file(data):
                result += OcrExtractor(file, data).result

        if result == '':
            logger.error(f'There are no resource files under the {self.task_name} task')
            self._result += '\tpass'
        else:
            self._result += result
        self._result += '\n\n'
        self.write_file()


class AllAssetsExtractor:
    def __init__(self):
        """
        获取./tasks目录下的所有任务文件夹，遍历每一个任务文件夹提取assets
        """
        logger.info('All assets extract')
        self.task_path = Path.cwd() / MODULE_FOLDER
        self.task_list = [x.name for x in self.task_path.iterdir() if x.is_dir()]

        self.task_paths = [str(x) for x in self.task_path.iterdir() if x.is_dir()]
        # 删除有Component的任务, 同时将其子路径加入任务列表
        self.task_paths = [x for x in self.task_paths if 'Component' not in x]
        self.task_paths.extend([str(x) for x in (self.task_path / 'Component').iterdir() if x.is_dir()])

        process_map(self.work, self.task_paths, max_workers=4)

    @staticmethod
    def work(task_path: str):
        me = AssetsExtractor(task_path)
        me.extract()


if __name__ == "__main__":
    AllAssetsExtractor()

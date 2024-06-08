from collections.abc import Iterator
from typing import Any, Union

class Setting(dict):
    settings = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if cls.settings is None:
            cls.settings = super().__new__(cls, *args, **kwargs)
        return cls.settings

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'attribute'):
            self.attribute = {}

    def __setitem__(self, key: Union[str], value: Union[dict, str, int, list]) -> None:
        if key not in self.attribute:
            self.attribute[key] = value
            # logger.debug("正在设置{}".format(key))
        else:
            pass

    def __getitem__(self, key: Union[str]) -> Any:
        return self.attribute.get(key, None)

    def get(self, key: Union[str], default: Any = None) -> Any:
        return self.attribute.get(key, default)

    def __str__(self) -> str:
        return str(self.attribute)

    def __iter__(self) -> Iterator:
        return iter(self.attribute)

# 测试代码
# s = Setting()
# s['123'] = False
# s['1232'] = 3
# print(s.get('123'))  # 输出: False
# print(s.get('1232'))  # 输出: 3
# print(s.get('non_existing_key', 'default_value'))  # 输出: default_value

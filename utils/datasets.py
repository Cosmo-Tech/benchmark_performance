from utils.singleton import SingletonType
from utils.constants import NAME

class DatasetsList(object, metaclass=SingletonType):
    list = []
    async def __set_datasets__(self, datasets):
        self.list.extend(datasets)

    async def __get_by_name__(self, name):
        dataset = list(filter(lambda d: d.get(NAME).lower() == name.lower(), self.list))
        if len(dataset) >= 1:
            return dataset[0]
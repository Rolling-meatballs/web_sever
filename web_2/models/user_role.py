import json
from enum import(
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    administer = auto()
    # enum UserRole:
    #      guest
    #      normal


class GuaEncoder(json.JSONEncoder):
    #"role":{
    #       "__enum__": "normal"
    #    }
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            # self.__class__.prefix
            # self.prefix
            return {self.prefix: o.name}
        else:
            return super().default(self, o)

def gua_decode(d):
    if GuaEncoder.prefix in d:
        name = d[GuaEncoder.prefix]
        return UserRole[name]
    else:
        return d

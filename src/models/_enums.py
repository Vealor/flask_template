import enum
################################################################################
# ENUMS

class Actions(enum.Enum):
    create = "create"
    modify = "modify"
    delete = "delete"

class Roles(enum.Enum):
    basic = "basic"
    admin = "admin"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

@dataclass_json
@dataclass(init=False)
class generics:
    name: str = ""
    module: str = ""
    id: t.List[int] = -1

    def __init__(self, *args):
        self.name = string_clean(args[0])
        self.module = string_clean(args[1])
        self.id = []
        for i in args[2:]:
            self.id.append(int(i))

        self.raw = args

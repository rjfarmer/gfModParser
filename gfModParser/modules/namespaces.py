@dataclass_json
@dataclass
class namespace:
    ref: int = -1

    def __post_init__(self):
        self.ref = symbol_ref(self.ref)


@dataclass_json
@dataclass(init=False)
class derived_ns:
    unknown1: str = None
    proc: t.List[typebound_proc] = None

    def __init__(self, *args, **kwargs):
        self.raw = args
        self.kwargs = kwargs

        if not len(args):
            return
        self.unknown1 = args[0]
        self.proc = []
        for i in args[1]:
            self.proc.append(typebound_proc(i))

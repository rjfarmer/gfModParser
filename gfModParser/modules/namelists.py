@dataclass_json
@dataclass(init=False)
class namelist:
    sym_ref: t.List[symbol_ref] = None

    def __init__(self, *args):
        self.raw = args
        self.sym_ref = []
        if len(args):
            for i in args:
                self.sym_ref.append(symbol_ref(i))

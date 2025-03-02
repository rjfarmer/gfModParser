@dataclass_json
@dataclass(init=False)
class formal_arglist:
    symbol: t.List[symbol_ref] = None

    def __init__(self, *args):
        self.symbol = []
        for i in args:
            self.symbol.append(symbol_ref(i))

        self.raw = args

    def __len__(self):
        return len(self.symbol)

    def __iter__(self):
        return iter(self.symbol)


@dataclass_json
@dataclass(init=False)
class typebound_proc:
    name: str = ""
    access: str = ""
    overridable: str = ""
    nopass: str = ""
    is_generic: str = ""
    ppc: str = ""
    pass_arg: str = ""
    pass_arg_num: symbol_ref = None
    proc_ref: symbol_ref = None

    def __init__(self, *args, **kwargs):
        self.name = string_clean(args[0][0])
        self.access = args[0][1][0]
        self.overridable = args[0][1][1]
        self.nopass = args[0][1][2]
        self.is_generic = args[0][1][3]
        self.ppc = args[0][1][4]
        self.pass_arg = string_clean(args[0][1][5])
        self.pass_arg_num = symbol_ref(args[0][1][6])

        # TODO: Handle is_generic
        self.proc_ref = symbol_ref(args[0][1][7][0])

        self.raw = args
        self.kwargs = kwargs


@dataclass_json
@dataclass(init=False)
class actual_arglist:
    def __init__(self, *args, **kwargs):
        self.raw = args
        self.kwargs = kwargs


@dataclass_json
@dataclass(init=False)
class attribute:
    flavor: str = ""
    intent: str = ""
    proc: str = ""
    if_source: str = ""
    save: str = ""
    ext_attr: int = -1
    extension: int = -1
    attributes: t.Set[str] = None

    def __init__(self, *args):
        self.flavor = string_clean(args[0])
        self.intent = string_clean(args[1])
        self.proc = string_clean(args[2])
        self.if_source = string_clean(args[3])
        self.save = string_clean(args[4])
        self.ext_attr = int(args[5])
        self.extension = int(args[6])
        self.attributes = set([string_clean(i) for i in args[7:]])
        self.raw = args

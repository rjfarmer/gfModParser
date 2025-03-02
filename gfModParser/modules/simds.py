@dataclass_json
@dataclass(init=False)
class simd_dec:
    args: None
    kwargs: None

    def __init__(self, *args, **kwargs):
        self.raw = args
        self.kwargs = kwargs

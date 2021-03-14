# GENS: Dict[Type, Callable[[ModelField], Any]] = {
#     str: lambda _f: "fake",
#     int: lambda _f: 1,
#     list: lambda _f: [],
#     bool: lambda _f: False,
#     BaseModel: lambda f: build_model(f.type_, factory=None, overrides={}),
#     Enum: lambda f: list(f.type_._member_map_.values())[0],
#     datetime: lambda f: datetime(2000, 1, 1)
# }

# def can_gen_default(field: ModelField) -> bool:
#     for type, _ in GENS.items():
#         if field.type_ == type or isinstance(field.type_, type) or issubclass(field.type_, type):
#             return True

#     return False


# def gen_default(field: ModelField) -> Any:
#     for type, gen_fn in GENS.items():
#         if field.type_ == type:
#             return gen_fn(field)

#     for type, gen_fn in GENS.items():
#         if isinstance(field.type_, type):
#             return gen_fn(field)

#     for type, gen_fn in GENS.items():
#         if issubclass(field.type_, type):
#             return gen_fn(field)


# def build_model(model: Type[BaseModel], factory: Any, overrides: Params) -> BaseModel:
#     return model(**build_fields(model, factory, overrides))


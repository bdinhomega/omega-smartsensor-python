from smartsensor import _def, _Serializer, R


def test_register_populated():
    for reg in R:
        if reg not in _def.keys():
            print(reg)


def test_register_def():
    for key, val in _def.items():
        if not issubclass(val['Data'], _Serializer):
            print(key)


test_register_populated()
test_register_def()
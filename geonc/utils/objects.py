import inspect


class GeoClass:
    pass


def make_list(v: list) -> list[any]:
    temp: list = []

    for e in v:
        if isinstance(e, dict):
            temp.append(GeoClass(e))

        elif isinstance(e, list):
            temp.append(make_list(e))
        
        else:
            temp.append(e)
    
    return temp


class GeoClass(dict):
    """
    Universal wrapper for any kind of dict item
    if the data structure change I won't have to do
    massive change in the code
    """
    def __init__(self, dico: dict):
        for k, v in dico.items():
            if isinstance(v, dict):
                setattr(self, k, GeoClass(v))
            
            elif isinstance(v, list):
                setattr(self, k, make_list(v))
            
            else:
                setattr(self, k, v)
        
    def __repr__(self):
        return str({k: v for k, v in self.__dict__.items()})

    def __getitem__(self, item: str | int):
        data = None

        if isinstance(item, str):
            data = getattr(self, item)

            if isinstance(data, list):
                if data and isinstance(data[0], GeoClass):
                    caller = inspect.stack()[1]
                    code = inspect.getsource(caller.frame).split("\n")[caller.lineno-1]
                    
                    if "]." not in code:
                        return [d.json for d in data]
            
        return data

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield str(k), v

    def items(self):
        return self.__dict__.items()
    
    def get(self, item, default=None):
        data = getattr(self, item)

        if data is None:
            return default
    
        return data
 
    @property
    def json(self):
        ignore: list = []

        dico: dict = {}

        for k, v in self.__dict__.items():
            if k in ignore:
                continue
            
            if isinstance(v, list):
                temp: list = []
                
                for e in v:
                    if isinstance(e, GeoClass):
                        temp.append(e.json)
                    
                    else:
                        temp.append(e)

                dico[k] = temp

            elif isinstance(v, GeoClass):
                dico[k] = v.json

            else:
                dico[k] = v

        return dico


def GeoObject(data: dict|list|GeoClass) -> GeoClass:
    if isinstance(data, list):
        return make_list(data)

    elif isinstance(data, dict):
        return GeoClass(data)

    elif isinstance(data, GeoClass):
        return data
    
    return data

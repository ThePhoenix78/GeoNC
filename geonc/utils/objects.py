class GeoClass(dict):
    """
    Universal wrapper for any kind of dict item
    if the data structure change I won't have to do
    massive change in the code
    """
    def __init__(self, dico: dict):

        for k, v in dico.items():
            self.__setitem__(k, v)

    def __setattr__(self, k, v):
        super().__setitem__(k, GeoObject(v))

    def __getattr__(self, k):
        return super().get(k)
        
    def __setitem__(self, k, v):
        super().__setitem__(k, GeoObject(v))


def GeoObject(data: dict|list|GeoClass) -> GeoClass:
    if isinstance(data, list):
        return [GeoObject(v) for v in data]

    elif isinstance(data, dict):
        return GeoClass(data)

    elif isinstance(data, GeoClass):
        return data
    
    return data
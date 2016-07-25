class IndexedList(list):
    """
    Class that combines a list and a dict into a single class
     - Written by Hugh Bothwell (http://stackoverflow.com/users/33258/hugh-bothwell)
     - Original source available at:
          http://stackoverflow.com/questions/5332841/python-list-dict-property-best-practice/5334686#5334686
     - Modifications by Jeff Terrace
    Given an object, obj, that has a property x, this allows you to create an IndexedList like so:
       L = IndexedList([], ('x'))
       o = obj()
       o.x = 'test'
       L.append(o)
       L[0] # = o
       L['test'] # = o
    """
    def __init__(self, items, attrs):
        super(IndexedList, self).__init__(items)
        # do indexing
        self._attrs = tuple(attrs)
        self._index = {}
        _add = self._addindex
        for obj in self:
            _add(obj)

    def _addindex(self, obj):
        _idx = self._index
        for attr in self._attrs:
            _idx[getattr(obj, attr)] = obj

    def _delindex(self, obj):
        _idx = self._index
        for attr in self._attrs:
            try:
                del _idx[getattr(obj, attr)]
            except KeyError:
                pass

    def __delitem__(self, ind):
        try:
            obj = list.__getitem__(self, ind)
        except (IndexError, TypeError):
            obj = self._index[ind]
            ind = list.index(self, obj)
        self._delindex(obj)
        return list.__delitem__(self, ind)

    def __delslice__(self, i, j):
        for ind in xrange(i, j):
            self.__delitem__(ind)

    def __getitem__(self, ind):
        try:
            return self._index[ind]
        except KeyError:
            if isinstance(ind, str):
                raise
            return list.__getitem__(self, ind)

    def get(self, key, default=None):
        try:
            return self._index[key]
        except KeyError:
            return default

    def __contains__(self, item):
        if item in self._index:
            return True
        return list.__contains__(self, item)

    def __getslice__(self, i, j):
        return IndexedList(list.__getslice__(self, i, j))

    def __setitem__(self, ind, new_obj):
        try:
            obj = list.__getitem__(self, ind)
        except (IndexError, TypeError):
            obj = self._index[ind]
            ind = list.index(self, obj)
        self._delindex(obj)
        self._addindex(new_obj)
        return list.__setitem__(ind, new_obj)

    def __setslice__(self, i, j, newItems):
        _get = self.__getitem__
        _add = self._addindex
        _del = self._delindex
        # remove indexing of items to remove
        for ind in xrange(i, j):
            _del(_get(ind))
        # add new indexing
        if isinstance(newItems, IndexedList):
            self._index.update(newItems._index)
        else:
            for obj in newItems:
                _add(obj)
        # replace items
        return list.__setslice__(self, i, j, list(newItems))

    def append(self, obj):
        self._addindex(obj)
        return list.append(self, obj)

    def extend(self, newList):
        newList = list(newList)
        if isinstance(newList, IndexedList):
            self._index.update(newList._index)
        else:
            _add = self._addindex
            for obj in newList:
                _add(obj)
        return list.extend(self, newList)

    def insert(self, ind, new_obj):
        # ensure that ind is a numeric index
        try:
            obj = list.__getitem__(self, ind)
        except (IndexError, TypeError):
            obj = self._index[ind]
            ind = list.index(self, obj)
        self._addindex(new_obj)
        return list.insert(self, ind, new_obj)

    def pop(self, ind= -1):
        # ensure that ind is a numeric index
        try:
            obj = list.__getitem__(self, ind)
        except (IndexError, TypeError):
            obj = self._index[ind]
            ind = list.index(self, obj)
        self._delindex(obj)
        return list.pop(self, ind)

    def remove(self, ind_or_obj):
        try:
            obj = self._index[ind_or_obj]
            ind = list.index(self, obj)
        except KeyError:
            ind = list.index(self, ind_or_obj)
            obj = list.__getitem__(self, ind)
        self._delindex(obj)
        return list.remove(self, ind)
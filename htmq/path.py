from keyboard import kwlist


class PathElement:

    def __init__(self, tag, all_=False, **attributes):
        self._path      = ''
        self._r_attrs   = {}
        self._count     = None
        self._tag       = tag

        self._process_attributes(all_, **attributes)


    def _process_attributes(self, all_, **attributes):
        self._path = '/' * (1 +all_) + self._tag
        attr_path = ''
        for name, value in attributes:
            if name.endswith('_r'):
                self._r_attrs[name[:-2]] = value
                continue
            elif name.endswith('_') and name[:-1] in kwlist:
                name = name[:-1]

            attr_path += "[@%s='%s']"%(name, value)

        if len(attr_path) > 0:
            self._path += attr_path


    def _set_count(self, n):
        self._count = n


    def _get_count(self):
        return self._count


    def _get_tag(self):
        return self._tag


    def _has_regex(self):
        return len(self._r_attrs) > 0


    def _get_path(self):
        return self._path


    tag         = property(_get_tag)
    count       = property(_get_count, _set_count)
    has_regex   = property(_has_regex)
    path        = property(_get_path)


class RootElement(PathElement):

    def __init__(self):
        PathElement.__init__(self, None)
        self._path = './'


    def _set_count(self, n):
        raise PathElementError('cannot set count on root element')


class HPath:

    def __init__(self):
        self._e = [RootElement()]
        self._all = False


    def add(self, tag, **attributes):
        e = PathElement(tag, **attributes, all_=self._all)
        self._all = False
        self._e.append(e)


    def find(self, etree):
        path = ''
        results = []

        for pe in self._e:
            if not pe.has_regex:
                path += pe.path



    def _findall(self, path, count, results):
        pass


    def _filter_r(self, results, r_attrs):
        pass


    def check_for_count(self):
        if len(e) < 1 or e[-1].count is not None:
            raise HPathError('redundant count on element: %s'%e[-1].tag)


    def all(self):
        if self._all:
            raise HPathError('redundant calls to all()')
        self._all = True


    def n(self, n):
        self.check_for_count()
        self._e[-1].count = n


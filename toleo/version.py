from toleo.utils import vstr_to_vtup


def rpm_compare(vstr1, vstr2):
    e1, v1, r1 = vstr_to_vtup(vstr1)
    e2, v2, r2 = vstr_to_vtup(vstr2)
    if (e1 or r1) and (e2 or r2):
        return rpm.labelCompare((e1, v1, r1), (e2, v2, r2))
    else:
        return rpm.labelCompare((None, v1, None), (None, v2, None))


def apt_compare(vstr1, vstr2):
    e1, v1, r1 = vstr_to_vtup(vstr1)
    e2, v2, r2 = vstr_to_vtup(vstr2)
    if (e1 or r1) and (e2 or r2):
        return apt_pkg.version_compare(vstr1, vstr2)
    else:
        return apt_pkg.version_compare(v1, v2)


def pacman_compare(vstr1, vstr2):
    e1, v1, r1 = vstr_to_vtup(vstr1)
    e2, v2, r2 = vstr_to_vtup(vstr2)
    if (e1 or r1) and (e2 or r2):
        return pyalpm.vercmp(vstr1, vstr2)
    else:
        return pyalpm.vercmp(v1, v2)


# Look for a system function to use for version comparisions.  Try to import
# rpm, apt_pkg, and pyalpm, in that order.  Once one suceeds, don't bother with
# the rest.
try:
    import rpm
except ImportError:
    try:
        import apt_pkg
    except ImportError:
        try:
            import pyalpm
        except ImportError:
            raise SystemExit('no suitable backend comparision method found')
        else:
            system_compare = pacman_compare
    else:
        apt_pkg.init_system()
        system_compare = apt_compare
else:
    system_compare = rpm_compare


class Version:
    """Version object that provides comparison methods.

    The comparision is based on differnet libraries depending on the system.

    RPM distributions: rpm module (python-rpm)
    APT distributions: apt_pkg module (apt-python)
    Pacman distributions: pyalpm module (pyalpm)
    """

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return '{}(\'{}\')'.format(self.__class__.__name__, self.__str__())

    def _check(self, other):
        if not isinstance(other, self.__class__):
            err = 'unorderable types: {}, {}'.format(
                self.__class__.__name__,
                other.__class__.__name__
            )
            raise TypeError(err)

    def __eq__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) == 0

    def __ne__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) != 0

    def __lt__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) < 0

    def __gt__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) > 0

    def __le__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) <= 0

    def __ge__(self, other):
        self._check(other)
        return system_compare(self.text, other.text) >= 0

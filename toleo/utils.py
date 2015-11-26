def vstr_to_vtup(vstr):
    i = vstr.find(':')
    if i == -1:
        epoch = None
    else:
        epoch = vstr[:i]
    i += 1
    j = vstr.rfind('-')
    if j == -1:
        version = vstr[i:]
        release = None
    else:
        version = vstr[i:j]
        release = vstr[j + 1:]
    return epoch, version, release


def vtup_to_vstr(vtup):
    e, v, r = vtup
    output = ''
    if e:
        output += '{}:'.format(e)
    output += v
    if r:
        output += '-{}'.format(r)
    return output

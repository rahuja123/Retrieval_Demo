import re
xac = re.compile(r'^S([-\d+])-B[-\d+]([ac])-([\w])$')
xb_ = re.compile(r'^S([-\d+])-B[-\d+]b-[\w]-([\w])$')
xb = re.compile(r'^S([-\d+])-B[-\d+]b-[\w]-([\w])[\w]$')
xEs = re.compile(r'^S2.[\d]-B[-\d+]-([\w])$')
xE = re.compile(r'^S2.[\d]-B[-\d+]-[\w]-([\w])$')

x1=0
x2=28
x3=42
x4=84
x5=100
x6=142
x7=178
x8=222
x9=250
x10=314
x11=352
x12=366
x13=410
x14=426



def get_x(name):
    res = xac.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1], res[2])
        if res[0]==1:
            if res[2]=='T':
                return x2
            elif res[2]=='B':
                return x5
        elif res[0]==2:
            if res[2]=='T':
                return x11
            elif res[2]=='B':
                return x14

    res = xb_.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1])
        if res[0]==1:
            if res[1]=='T':
                return x3
            elif res[1]=='B':
                return x4
        elif res[0]==2:
            if res[1]=='T':
                return x12
            elif res[1]=='B':
                return x13

    res = xb.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1])
        if res[0]==1:
            if res[1]=='T':
                return x2
            elif res[1]=='B':
                return x5
        elif res[0]==2:
            if res[1]=='T':
                return x11
            elif res[1]=='B':
                return x14

    res = xEs.match(name)
    if res is not None:
        res = res.groups()
        res = (res[0],)
        if res[0]=='T':
            return x6
        elif res[0]=='B':
            return x10

    res = xE.match(name)
    if res is not None:
        res = res.groups()
        res = (res[0],)
        if res[0]=='T':
            return x7
        elif res[0]=='B':
            return x9
        elif res[0]=='M':
            return x8

    raise ValueError('Invalid camera name.')



yac = re.compile(r'^S([-\d+])-B[-\d+]([ac])-([\w])$')
yb_ = re.compile(r'^S[-\d+]-B[-\d+]b-([\w])-[\w]$')
yb = re.compile(r'^S[-\d+]-B[-\d+]b-([\w])-[\w]([\w])$')
yE = re.compile(r'^S2.([-\d+])-B[-\d+]-([\w])$')
yEs = re.compile(r'^S2.([-\d+])-B[-\d+]-([\w])-[\w]$')

y1=0
y2=50
y3=165
y4=194
y5=225
y6=359
y7=388
y8=420
y9=558
y10=348
y11=428
y12=490
y13=586


def get_y(name):
    res = yac.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1], res[2])
        if res[1]=='c':
            return y2
        elif res[1]=='a':
            return y9

    res = yb_.match(name)
    if res is not None:
        res = res.groups()
        res = (res[0],)
        if res[0]=='L':
            return y4
        elif res[0]=='R':
            return y7

    res = yb.match(name)
    if res is not None:
        res = res.groups()
        if res[0]=='L':
            if res[1]=='L':
                return y3
            elif res[1]=='R':
                return y5
        elif res[0]=='R':
            if res[1]=='L':
                return y6
            elif res[1]=='R':
                return y8

    res = yE.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1])
        if res[0]==1:
            if res[1]=='T':
                return y10
            elif res[1]=='B':
                return y11
        elif res[0]==2:
            if res[1]=='T':
                return y13
            elif res[1]=='B':
                return y12

    res = yEs.match(name)
    if res is not None:
        res = res.groups()
        res = (int(res[0]), res[1])
        if res[0]==1:
            if res[1]=='L':
                return y10
            elif res[1]=='R':
                return y11
        elif res[0]==2:
            if res[1]=='R':
                return y13
            elif res[1]=='L':
                return y12

    raise ValueError('Invalid camera name.')


def get_coordinate(cam_name):
    '''
    Return the coordinates of the camera:
        x : column index of picture
        y : row index of the picture
    '''
    return get_y(cam_name), get_x(cam_name)



c_ac = re.compile(r'^S([-\d+])-B[-\d+]([ac])-[\w]$')
c_b_ = re.compile(r'^S([-\d+])-B[-\d+]b-([\w])-([\w])$')
c_b = re.compile(r'^S([-\d+])-B[-\d+]b-([\w])-([\w])[\w]$')
c_E = re.compile(r'^S2.([-\d+])-B[-\d+]-([\w])$')
c_Es = re.compile(r'^S2.([-\d+])-B[-\d+]-([\w])-[\w]$')


def get_cluster(cam_name):
    res = c_ac.match(cam_name)
    if res is not None:
        res = res.groups()
        return "S{}-{}".format(res[0], res[1])

    res = c_b_.match(cam_name)
    if res is not None:
        res = res.groups()
        if res[2]=='T':
            return "S{}-b-{}-{}".format(res[0], res[1], 'B')
        elif res[2]=='B':
            return "S{}-b-{}-{}".format(res[0], res[1], 'T')

    res = c_b.match(cam_name)
    if res is not None:
        res = res.groups()
        return "S{}-b-{}-{}".format(res[0], res[1], res[2])

    res = c_E.match(cam_name)
    if res is not None:
        res = res.groups()
        return "S2.{}-{}".format(res[0], res[1])

    res = c_Es.match(cam_name)
    if res is not None:
        res = res.groups()
        return "S2.{}-{}".format(res[0], res[1])

    raise ValueError('Invalid camera name.')



_cac = re.compile(r'^S([-\d+])-([ac])$')
_cb = re.compile(r'^S([-\d+])-b-([\w])-([\w])$')
_cE = re.compile(r'^S2.([-\d+])-([\w])$')

def _mean(*ps):
    ps = [get_coordinate(p) for p in ps]
    return sum([p[0] for p in ps])/len(ps), sum([p[1] for p in ps])/len(ps)


def get_cluster_position(cluster_name):
    res = _cac.match(cluster_name)
    if res is not None:
        res = res.groups()
        p1 = "S{}-B1{}-T".format(res[0], res[1])
        p2 = "S{}-B1{}-B".format(res[0], res[1])
        return _mean(p1,p2)

    res = _cb.match(cluster_name)
    if res is not None:
        res = res.groups()
        p1 = "S{}-B1b-{}-{}L".format(res[0], res[1], res[2])
        p2 = "S{}-B1b-{}-{}R".format(res[0], res[1], res[2])
        return _mean(p1,p2)

    res = _cE.match(cluster_name)
    if res is not None:
        res = res.groups()
        if res[1]=="T" or res[1]=="B":
            p = "S2.{}-B1-{}".format(res[0], res[1])
            return _mean(p)
        elif res[1]=="L" or res[1]=="R":
            p1 = "S2.{}-B1-{}-T".format(res[0], res[1])
            p2 = "S2.{}-B1-{}-B".format(res[0], res[1])
            return _mean(p1, p2)

    raise ValueError('Invalid camera name.')


if __name__ == '__main__':
    assert get_coordinate('S1-B3b-L-T')==(194, 42)
    assert get_coordinate('S2.1-B2-L-T')==(348, 178)
    assert get_coordinate('S2-B5a-T')==(558, 352)
    assert get_coordinate('S2.2-B3-R-M')==(586, 222)
    assert get_coordinate('S2-B5c-B')==(50, 426)
    # assert get_coordinate('S2-B5b-L-TR')==(50, 426)

    assert get_cluster('S1-B3b-L-T')=='S1-b-L-B'
    assert get_cluster('S2.1-B2-L-T')=='S2.1-L'
    assert get_cluster('S2-B5a-T')=='S2-a'
    assert get_cluster('S2.2-B3-R-M')=='S2.2-R'
    assert get_cluster('S2-B5c-B')=='S2-c'

    # assert get_cluster_position

    print(get_cluster_position(get_cluster("S2.1-B4-T")))

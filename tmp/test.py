class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)


class Rectangle(object):
    def __init__(self, posn, w, h):
        self.corner = posn
        self.width = w
        self.height = h

    def __str__(self):
        return "({0},{1},{2})".format(self.corner, self.width, self.height)

    def contains(self, point):
        return (self.corner.x <= point.x <= self.corner.x + self.width and
                self.corner.y <= point.y <= self.corner.y + self.height)


f = Rectangle(Point(48.870106, 2.146403), 0.2, 0.10)
tmp = Point(48.876429, 2.211978)
tmp2 = Point(48.960051, 2.236728)
print f
print tmp2
if f.contains(tmp):
    print "inside"
else:
    print "outside"

if f.contains(tmp2):
    print "inside"
else:
    print "outside"

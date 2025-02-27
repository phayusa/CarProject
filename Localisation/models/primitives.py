class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    class Meta:
        abstract = True


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

    class Meta:
        abstract = True


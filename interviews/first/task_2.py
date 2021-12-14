class MySet:

    seq = list()

    def __init__(self, list=None):

        # todo parent hash
        hash()

        if not list:
            self.

        self.seq = list

    def add(self, elem):

        if elem not in self.seq:
            self.seq.append(elem)

        return self

    def remove(self, value):

        if value in self.seq:
            self.seq.remove(value)


if __name__ == '__main__':
    i = 'q'
    s = 'w'

    my_set = MySet()
    my_set.add(i)
    print(my_set.seq)
    my_set.add(s)
    print(my_set.seq)

    my_set.remove('q')
    print(my_set.seq
          )
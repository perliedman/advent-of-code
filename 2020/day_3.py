class Grid:
    def __init__(self, lines):
        self.lines = [l.strip() for l in lines if len(l) > 1]
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def is_tree(self, x, y):
        return self.lines[y][x % self.width] == '#'

    def count_trees(self, dx, dy):
        x = y = 0
        tree_count = 0
        while y < self.height:
            if self.is_tree(x, y):
                tree_count = tree_count + 1
            
            x = x + dx
            y = y + dy

        return tree_count

    def __str__(self):
        return '\n'.join(['========='] + self.lines + ['========='])

if __name__ == '__main__':
    import sys

    with open(sys.argv[1], 'r') as f:
        grid = Grid(f.readlines())

    dirs = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]

    r = None
    for dx, dy in dirs:
        count = grid.count_trees(dx, dy)
        print(dx, dy, count)
        r = r * count if r else count

    print(r)


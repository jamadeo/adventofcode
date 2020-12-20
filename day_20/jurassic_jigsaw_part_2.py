import fileinput
import sys

import numpy as np


sea_monster_mask = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

sea_monster_mask = np.array([list(r) for r in sea_monster_mask]) == '#'
print(np.shape(sea_monster_mask))

def read_sections(lines):
    section = []
    for line in lines:
        line = line.rstrip()
        if line == '':
            yield section
            section = []
        else:
            section.append(line)
    yield section


def read_tiles(lines):
    for section in read_sections(lines):
        assert section[0].startswith('Tile'), section[0]
        tile_id = section[0].split(' ')[1][:-1]
        img = np.array([list(s) for s in section[1:]]) == '#'
        yield tile_id, img.astype(int)


tiles = {
    tile_id: tile for tile_id, tile in read_tiles(fileinput.input(sys.argv[1]))
}

solution = {}

for row in fileinput.input(sys.argv[2]):
    x, y, tile_id, flip, rotate = row.split(' ')
    solution[(int(x), int(y))] = (tile_id, flip, rotate)

size = max(x for x, y in solution.keys()) + 1
rows = []
for x in range(size):
    row = []
    for y in range(size):
        tile_id, flip, rotate = solution[(x, y)]
        tile = tiles[tile_id]
        if int(flip):
            tile = np.flip(tile, axis=1)
        tile = np.rot90(tile, k=int(rotate) + 3)  # TODO: what went wrong here?
        row.append(tile[1:-1,1:-1])
    rows.append(np.hstack(row))


img = np.vstack(rows)
print(img)

sm_x, sm_y = np.shape(sea_monster_mask)
img_x, img_y = np.shape(img)

total_hashes = np.sum(img)
print('total', total_hashes)
for do_flip, img in enumerate((img, np.flip(img, axis=1))):
    for rotate in range(4):
        im = np.rot90(img, k=rotate)
        print(f'{do_flip=} {rotate=}')
        if do_flip and rotate == 0:
            print(im)
        monsters = 0
        for x in range(img_x - sm_x + 1):
            for y in range(img_y - sm_y + 1):
                region = im[x:x+sm_x,y:y+sm_y]
                has_sea_monster = (region[sea_monster_mask] == 1).all()
                if has_sea_monster:
                    monsters += 1
                    print(f'\tsea monster at {x=}, {y=}')
        if monsters:
            print(total_hashes - monsters * np.sum(sea_monster_mask.astype(int)))


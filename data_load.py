import numpy as np
from tqdm import tqdm

#---------------------Import coordinate file-------------------------#
f_x = 'x.txt'
f_l = 'l.txt'

x = np.loadtxt(f_x, dtype=int)
l = np.loadtxt(f_l, dtype=int)

#-------------------Column Parameters---------------------------------#
L = 40  # length of column
w = 5  # width of column
#-------------------Generate Image-------------------------------------#


def img_gen(L, w, x, l, ii):
    # L and w are coumn dimensions
    # x and l are files to generate geometry
    # ii  is the column number to be generated
    x = x
    l = l
    img = np.zeros((L, w), dtype=int)

    img[0, 0:w] = 1
    img[-1, 0:w] = 1

    for jj in range(1, L-1):
        img[jj, x[ii][jj]-l[ii][jj]:x[ii][jj]+l[ii][jj]] = 1

    return img


img = []
print('Loading dataset...', flush=True)
for ii in tqdm(range(25000)):
    # img ouput, save  as array of images if want to convert to graph
    img.append(img_gen(L, w, x, l, ii))

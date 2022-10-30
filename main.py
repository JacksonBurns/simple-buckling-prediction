import numpy as np
from tqdm import tqdm
from data_load import img

APPROACH = 'CLUSTERED_WEIGHTED_CUTS' #'CUMULATIVE_CENTERMOST_DEEPEST' # 'CENTERMOST_DEEPEST_CUT'  # 'MASS'

labels = np.loadtxt('subdataset1_labels.txt', dtype=int)

predictions = np.zeros((25000,))
tied_count = 0
print('Generating Predictions...', flush=True)
for i in tqdm(range(25000)):
    if APPROACH == 'CENTERMOST_DEEPEST_CUT':
        max_left_cut = 0
        for row in range(40):
            # find the first 1
            cut=np.where(img[i][row] == 1)[0][0]
            if row+1<=20:
                weighted_cut = cut*(row+1)
            else:
                weighted_cut = cut*(abs(40-row))
            if  weighted_cut > max_left_cut:
                max_left_cut = cut
        
        max_right_cut = 0
        for row in range(40):
            cut=np.where(np.flip(img[i][row]) == 1)[0][0]
            if row+1<=20:
                weighted_cut = cut*(row+1)
            else:
                weighted_cut = cut*(abs(40-row))
            if  weighted_cut > max_right_cut:
                max_right_cut = cut
        
        if max_left_cut < max_right_cut:
            predictions[i] = 1
    
    elif APPROACH == 'CLUSTERED_WEIGHTED_CUTS':
        # side with the longest contiuous, deepest cut will bend in other direction
        pass
    elif APPROACH == 'STEEPEST_CUT':
        # use element wise differentiation and find the area with the steepest change
        pass
    elif APPROACH == 'CUMULATIVE_CENTERMOST_DEEPEST':
        left_cut_count = 0
        for row in range(40):
            # find the first 1
            cut=np.where(img[i][row] == 1)[0][0]
            if row+1<=20:
                weighted_cut = cut*(row+1)
            else:
                weighted_cut = cut*(abs(40-row))
            left_cut_count += weighted_cut**4
        
        right_cut_count = 0
        for row in range(40):
            cut=np.where(np.flip(img[i][row]) == 1)[0][0]
            if row+1<=20:
                weighted_cut = cut*(row+1)
            else:
                weighted_cut = cut*(abs(40-row))
            right_cut_count += weighted_cut**4
        
        if left_cut_count > right_cut_count:
            predictions[i] = 1


    elif APPROACH == 'MASS':
        # sum down the columns
        col_sum = np.sum(img[i], 0)
        # if there are more blocks on the left, it will fail to the right
        if np.sum(col_sum[0:2]) > np.sum(col_sum[3: 5]):
            predictions[i] = 1


result = np.logical_not(np.logical_xor(labels, predictions))
correct_count = np.count_nonzero(result)
print('{:} correct out of 25000 ({:.2f}%)'.format(
    correct_count, 100*correct_count/25000))
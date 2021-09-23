import os
import numpy as np
import pandas as pd
from ccdc.io import CrystalReader
from ccdc.crystal import PackingSimilarity
'''
Initial run 9x9 with duplicate comparisons: 516.1s

Run without duplicate comparison 270.4s
'''
directory = r'C:\Users\Clamfighter\Machine_Learning_Project\my_env\Masters\T2_9_experimental_crystals\T2_9_experimental_crystals'
PS = PackingSimilarity()
i=0
cifs = []


for filename in os.listdir(directory):
    cifs.append(filename)
#rmsd_matrix = np.empty((len(cifs),len(cifs)))
rmsd_matrix = np.empty((9,9))
print('MATRIX: ')
print(rmsd_matrix)
print(len(cifs))
cols = cifs
for i in range(len(cifs)):
    outter_cif = cifs[i]
    print(i)
    print(outter_cif)

    crystal_reader = CrystalReader(directory+'\\'+outter_cif)
    outter_crystal = crystal_reader[0]
    for j in range(len(cifs)):
        inner_cif = cifs[j]
        if inner_cif != outter_cif and inner_cif != "":
            print(outter_cif +' / '+inner_cif)
            
            crystal_reader = CrystalReader(directory+'\\'+inner_cif)
            inner_crystal = crystal_reader[0]
            comp = PS.compare(outter_crystal,inner_crystal)
            rmsd = comp.rmsd
            print('column: ',i)
            print('row: ',j)
            print('rmsd: ',rmsd)
            rmsd_matrix[i][j] = rmsd
            print(rmsd_matrix)
        elif inner_cif == outter_cif:
            print(outter_cif +' / '+inner_cif + ' MATCH')
    cifs[i] = ""
    i+=1
df = pd.DataFrame(rmsd_matrix, columns=cols, index=cols)
print(df)
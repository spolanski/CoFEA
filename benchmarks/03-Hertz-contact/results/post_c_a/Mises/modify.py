import glob as gb
import os, shutil
result_file_names = gb.glob("*.csv")
cwd = os.getcwd()
for result in result_file_names:
    shutil.copyfile(cwd + '/' + result,
        cwd + '/csvs/' + result.replace('_mises.csv','_codeaster_mises.csv'))


# import shutil
# import os
# src = r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Work\name.txt'
# dst =  r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Newfolder\name.txt'
# shutil.copyfile(src, dst)
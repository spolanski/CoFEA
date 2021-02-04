import pandas
import matplotlib.pyplot as pl

files_to_read = ["Regular_Linear_1_to_10.txt",
                 "Regular_Quadratic_1_to_10.txt",
                 "Unregular_Linear_1_to_20.txt",
                 "Unregular_Quadratic_1_to_10.txt"]

df = {}
fig1 = pl.figure()
ax = pl.gca()
for file_to_read in files_to_read:
    df[file_to_read] = pandas.read_csv(file_to_read, header=None)
    df[file_to_read].plot(x=0, y=1, ax=ax, marker = "o", label = file_to_read )

pl.xlabel("Number of nodes")
pl.ylabel("Y normal stress in point D")
pl.grid()
pl.show()
print(df)

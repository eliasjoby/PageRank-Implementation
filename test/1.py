import csv
filename="characters-nodes.csv"

fields=[]
rows=[]

with open(filename,'r') as fobj:
    ro=csv.reader(fobj)

    fields=next(ro)

    for row in ro:
        rows.append(row)
    
    print("Total no. of rows with info: %d" % (ro.line_num-1))

print("Field Names are: "+','.join(fields))

print("\nThe first 6 rows with info are:\n")

for row in rows[:6]:
    for col in row:
        print("%s" % col,end=" ")
    print("\n")

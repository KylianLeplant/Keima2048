#*******
#* Read input from STDIN
#* Use print to output your result to STDOUT.
#* Use sys.stderr.write() to display debugging information to STDERR
#* ***/
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))
phrase = lines[0]
lis = []
var_bool = False
for i in phrase:
    print(i,lis)
    try :
        if type(int(i)) == int:
            lis.append(i)
    except:
        pass
    if i == "+":
        lis.append(int(lis[0])+int(lis[1]))
        del lis[0]
        del lis[1]
    elif i == "*":
        lis.append(int(lis[0])*int(lis[1]))
        del lis[0]
        del lis[1]
    elif i == ">" and var_bool:
        lis.append(int(lis[1]))
        lis.append(int(lis[0]))
        del lis[0]
        del lis[1]
    elif i == "-":
        try:
            lis.append(-int(lis[0]))
            except:
                print(str(lis))
        del lis[0]
    if i == "<":
        var_bool = True
    elif i == " ":pass
    else:
        var_bool = False
    
print(lis,phrase)
#http://sbirch.net/tidbits/context_menu.html
#shell:sendto
import os
from sys import argv
from tabulate import tabulate
import re
import math
from msvcrt import getch

# http://patorjk.com/software/taag/#p=display&f=Small%20Slant&t=DATA%20BUILDER
header_1 = "\
\n\
     ___  ___ _________     ___  __  ________   ___  _______  \n\
    / _ \/ _ /_  __/ _ |   / _ )/ / / /  _/ /  / _ \/ __/ _ \ \n\
   / // / __ |/ / / __ |  / _  / /_/ // // /__/ // / _// , _/ \n\
  /____/_/ |_/_/ /_/ |_| /____/\____/___/____/____/___/_/|_|  \n"

colors = {
    'blue': '\033[94m',
    'pink': '\033[95m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'turquoise': '\033[96m',
    'gray': '\033[32m',
}

script, filename = argv
version = 'version 0.1'
headers1 = ["LABEL", "X", "Y", "Z"]
headers2 = ["!LABEL", "X", "Y", "Z"]
headers3 = ["INDEX","LABEL", "X", "Y", "Z"]
headers4 = ["LABEL", "X", "Y", "Z","DIST", "X", "Y", "Z"]
headers5 = ["INDEX","LABEL", "X", "Y", "Z","DIST", "X", "Y", "Z"]

def colorize(string, color):
    if color not in colors:
        return string
    else:
        return colors[color] + string + '\033[0m'

def filecheck():
    ext = ['stp', 'step']
    if filename.split('.')[-1] in ext:
        return('File OK')
    else:
        return('BAD FILE')

def getpoints(precision,skip_pnt = True):
    table = []
    with open(filename) as f:
        line = f.readline()
        while line:
            for i in line:
                if 'CARTESIAN_POINT' in line:
                    if "''"  in line or 'centre point' in line:
                        pass
                    else:
                        if 'PNT' in line and skip_pnt == True:
                            pass
                        else:
                            item = []
                            a = (line.split('(',1)[-1]).rstrip("\n\r") #remove up to first parenthesis and EOL
                            b = re.sub("[();']",'', a) #remove other characters
                            c = (b.split(',')) #convert to list separated by ','
                            if c[3] == '':
                                pass
                            else:
                                item.append(c[0]) #Label
                                item.append("{:.{}f}".format(float(c[1]), precision)) #X
                                item.append("{:.{}f}".format(float(c[2]), precision)) #Y
                                item.append("{:.{}f}".format(float(c[3]), precision)) #Z
                                table.append(item)
                line = f.readline()
    return(table)

def portrait():
    os.system('cls')
    print(colorize(header_1, 'pink'))
    print(colorize(version, 'green'))
    print()

def local_help():
    a = '##### display help here #####'
    portrait()
    print(a)
    input("Press [Enter] to continue...")
    main()

def decimals():
    portrait()
    print(colorize('Enter number of decimals required, default 3', 'turquoise'))
    precision = input(colorize('>>','pink'))
    if precision == '':
        precision = 3
    elif precision.isdigit():
        precision = int(precision)
    elif precision.lower() == 'q':
        os.system('cls')
        exit()
    else:
        input('Oops!  That was no valid option. Try again...')
        main()
    return(precision)

def showpoints():
    portrait()
    precision = decimals()
    table = getpoints(precision)
    portrait()
    print(colorize('FILE OK -->','green'),colorize(filename,'green'))
    print(tabulate(table,headers1, tablefmt="pretty", floatfmt=('.'+str(precision)+'f')))
    print()
    minimenu(table,precision)

def showpoints_pnt():
    portrait()
    precision = decimals()
    table = getpoints(precision,skip_pnt = False)
    portrait()
    print(colorize('FILE OK -->','green'),colorize(filename,'green'))
    print(tabulate(table,headers1, tablefmt="pretty", floatfmt=('.'+str(precision)+'f')))
    print()
    minimenu(table,precision)

def savetxt(table,precision,rot = False):
    if rot == True:
        head = headers4
    else:
        head = headers2
    portrait()
    print(tabulate(table,head, tablefmt="plain", floatfmt=('.'+str(precision)+'f')))
    file = open('table.txt', 'w')
    file.write(tabulate(table,head, tablefmt="plain", floatfmt=('.'+str(precision)+'f')))
    file.close()
    print(colorize('file saved as table.txt','green'))
    input(colorize('Press any key to exit...','green'))
    exit()

def saveptb(table,precision):
    portrait()
    table2 = []
    for i, key in enumerate(table):
        if i == 0:
            pass
        else:
            key.pop(0)
            key.insert(0,i)
            table2.append(key)
    print(tabulate(table2,headers2, tablefmt="plain", floatfmt=('.'+str(precision)+'f')))
    file = open('table.ptb', 'w')
    file.write(tabulate(table2,headers2, tablefmt="plain", floatfmt=('.'+str(precision)+'f'),numalign="left"))
    file.close()
    print(colorize('file saved as table.ptb','green'))
    input(colorize('Press any key to exit...','green'))
    exit()

def createtrailfile(table,precision):
    portrait()
    label_1 = "~ Select `Odui_Dlg_00` `t1.CSysPntsTbl` 2 `okit_wdg_table_row_"
    row = 0
    label_2 = "` `Name`"
    label_3 = "~ Activate `Odui_Dlg_00` `t1.rename`"
    label_4 = "~ Update `Odui_Dlg_00` `t1.PntNameInpPnl` `"
    label_5 = "`"
    x_1 = "~ Select `Odui_Dlg_00` `t1.CSysPntsTbl` 2 `okit_wdg_table_row_"
    x_2 = "` `Axis1`"
    x_3 = "~ Update `Odui_Dlg_00` `t1.OffsetValInpPnl` `"
    x_4 = "`"
    x_5 = "` `Axis2`"
    x_6 = "` `Axis3`"
    with open("table-trail.txt", 'w') as g:
        for j in table:
            g.write(label_1 + str(row) + label_2 + '\n')
            g.write(label_1 + str(row) + label_2 + '\n')
            g.write(label_3 + '\n')
            g.write(label_4 + str(j[0]) + label_5 + '\n')
            g.write(x_1 + str(row) + x_2 + '\n')
            g.write(x_3 + str(j[1]) + x_4 + '\n')
            g.write(x_1 + str(row) + x_5 + '\n')
            g.write(x_3 + str(j[2]) + x_4 + '\n')
            g.write(x_1 + str(row) + x_6 + '\n')
            g.write(x_3 + str(j[3]) + x_4 + '\n')
            row +=1
    print(colorize('file saved as table-trail.txt','green'))
    input(colorize('Press any key to exit...','green'))
    exit()

def popfromlist(table,precision,rot = False):
    if rot == True:
        head = headers5
    else:
        head = headers3
    while True:
        portrait()
        print(tabulate(table,head, tablefmt="pretty", floatfmt=('.'+str(precision)+'f'),showindex="always"))
        print(colorize('Enter row to delete, D for done or Q to exit', 'green'))
        print(colorize("Ex. '9' will delete row with index 9", 'green'))
        print(colorize("Ex. '5-12' will delete all rows from 5 up to 12 ", 'green'))
        print(colorize('When done press D to follow further processing', 'green'))
        delete_index = input(colorize('>>','green'))
        if delete_index.lower() == 'q':
            exit()
        if delete_index.lower() == 'd':
            if rot == True:
                minimenu2(table,precision,rot)
            else:
                minimenu(table,precision)
        if ',' in delete_index:
            lst_delete_index = delete_index.split(',')
            lst_delete_index.sort(reverse=True)
            for i in lst_delete_index:
                table.pop(int(i))
        if '-' in delete_index:
            lst_delete_index = delete_index.split('-')
            lst_delete_index.sort
            new_delete_lst = []
            for _ in range((int(lst_delete_index[-1])-int(lst_delete_index[0]))+1):
                new_delete_lst.append(int(lst_delete_index[0])+_)
            new_delete_lst.sort(reverse=True)
            for i in new_delete_lst:
                table.pop(int(i))
        if delete_index.isdigit() and int(delete_index) < len(table):
            table.pop(int(delete_index))

def rearrange(table,precision,rot = False):
    if rot == True:
        head = headers5
    else:
        head = headers3
    while True:
        portrait()
        print(tabulate(table,head, tablefmt="pretty", floatfmt=('.'+str(precision)+'f'),showindex="always"))
        print(colorize('Enter row to move, D for done or Q to exit', 'green'))
        move_index = input(colorize('>>','green'))
        if move_index.lower() == 'q':
            exit()
        if move_index.lower() == 'd':
            if rot == True:
                minimenu2(table,precision,rot)
            else:
                minimenu(table,precision)
        if move_index.isdigit() and int(move_index) < len(table):
            move_index = int(move_index)
            while True:
                portrait()
                print(tabulate(table,head, tablefmt="pretty", floatfmt=('.'+str(precision)+'f'),showindex="always"))
                print(colorize('Enter D for done', 'green'))
                print(colorize('Press W to move row up', 'green'))
                print(colorize('Press S to move row down', 'green'))
                #up_down = input('>>')
                up_down = (str(list(str(getch()))[2]))
                if up_down.lower() == 'd':
                    break
                if up_down.lower() == 'w':
                    table.insert(move_index-1, table.pop(move_index))
                    move_index-=1
                if up_down.lower() == 's':
                    table.insert(move_index+1, table.pop(move_index))
                    move_index+=1

def rotate(x,y,z,XROT,YROT,ZROT):
    X1 = x
    Y1 = y
    Z1 = z
    X2=((X1*math.cos(YROT)+(Y1*math.sin(XROT)+Z1*math.cos(XROT))*math.sin(YROT))*math.cos(ZROT)-(Y1*math.cos(XROT)-Z1*math.sin(XROT))*math.sin(ZROT))
    Y2=((X1*math.cos(YROT)+(Y1*math.sin(XROT)+Z1*math.cos(XROT))*math.sin(YROT))*math.sin(ZROT)+(Y1*math.cos(XROT)-Z1*math.sin(XROT))*math.cos(ZROT))
    Z2=(-X1*math.sin(YROT)+(Y1*math.sin(XROT)+Z1*math.cos(XROT))*math.cos(YROT))
    return(X2,Y2,Z2)

def dist(x1,y1,z1,x2=0,y2=0,z2=0):
    return(math.sqrt(math.pow(float(x1)-float(x2),2)+math.pow(float(y1)-float(y2),2)+math.pow(float(z1)-float(z2),2)))

def rotateddata(table,precision): #verified here https://keisan.casio.com/exec/system/15362817755710
    while True:
        try:
            portrait()
            XROT = float(input(colorize('Enter X rotation >>', 'green')))
            if isinstance(XROT, (int, float)):
                portrait()
                YROT = float(input(colorize('Enter Y rotation >>', 'green')))
                if isinstance(YROT, (int, float)):
                    portrait()
                    ZROT = float(input(colorize('Enter Z rotation >>', 'green')))
                    if isinstance(ZROT, (int, float)):
                        portrait()
                        print(colorize('X rotation {0}'.format(XROT), 'green'))
                        print(colorize('Y rotation {0}'.format(YROT), 'green'))
                        print(colorize('Z rotation {0}'.format(ZROT), 'green'))
                        if input(colorize('Are this coordinates correct Y/N?','green')).lower() == 'y':
                            break
        except ValueError:
            input(colorize('Enter numbers only!','red'))
    ct=0
    for row in table:
        rotated_data = list(rotate(float(row[1]),float(row[2]),float(row[3]),XROT,YROT,ZROT))
        for i in rotated_data:
            row.append("{:.{}f}".format(float(i), precision))
    for i in range(len(table)):
        if len(table)-1 == ct:
            distance = "{:.{}f}".format(float(dist(table[ct][1],table[ct][2],table[ct][3])), precision)
        else:
            distance = "{:.{}f}".format(float(dist(table[ct][1],table[ct][2],table[ct][3],table[(ct+1)][1],table[(ct+1)][2],table[(ct+1)][3])), precision)
        table[ct].insert(4,distance)
        ct +=1
    portrait()
    print(tabulate(table,headers4, tablefmt="fancy_grid", floatfmt=('.'+str(precision)+'f')))
    minimenu2(table,precision)

def minimenu(table,precision):
    menuItems2 = {
    'Save points to text file': savetxt,
    'Save points to ptb file': saveptb,
    'Create trail file' : createtrailfile,
    'Remove points from list': popfromlist,
    'Rearrange points from list': rearrange,
    'Add rotation and show points': rotateddata
    }
    check_num2 = [0, 1, 2, 3, 4, 5] #numero de opciones
    for i, key in enumerate(menuItems2):
        print(colorize('[' + str(i) + '] ', 'yellow'), list(menuItems2.keys())[i])
    print(colorize('[Q]', 'red') + '  QUIT')
    choices = input(">> ")
    if choices.lower() == 'q':
        os.system('cls')
        exit()
    if choices.isdigit():
        if int(choices) in check_num2:
            menuItems2[list(menuItems2.keys())[int(choices)]](table,precision)
        else:
            input('Oops!  That was no valid option. Try again...')
            main()
    else:
        input('Oops!  That was no valid option. Try again...')
        main()

def minimenu2(table,precision,rot=True):
    menuItems2 = {
    'Save points to text file': savetxt,
    'Remove points from list': popfromlist,
    'Rearrange points from list': rearrange,
    }
    check_num2 = [0, 1, 2] #numero de opciones
    for i, key in enumerate(menuItems2):
        print(colorize('[' + str(i) + '] ', 'yellow'), list(menuItems2.keys())[i])
    print(colorize('[Q]', 'red') + '  QUIT')
    choices = input(">> ")
    if choices.lower() == 'q':
        os.system('cls')
        exit()
    if choices.isdigit():
        if int(choices) in check_num2:
            menuItems2[list(menuItems2.keys())[int(choices)]](table,precision,rot)
        else:
            input('Oops!  That was no valid option. Try again...')
            main()
    else:
        input('Oops!  That was no valid option. Try again...')
        main()

def main():
    menuItems = {
    'Show points': showpoints,
    'Show all points including "PNT"' : showpoints_pnt,
    }
    while True:
        check_num = [0, 1] #numero de opciones
        portrait()
        if filecheck() == 'File OK':
            print(colorize('FILE OK -->','green'),colorize(filename,'green'))
            for i, key in enumerate(menuItems):
                print(colorize('[' + str(i) + '] ', 'yellow'), list(menuItems.keys())[i])
            #print(colorize('[H]', 'yellow') + '  HELP')
            print(colorize('[Q]', 'red') + '  QUIT')
            choices = input(">> ")
            if choices.lower() == 'q':
                os.system('cls')
                exit()
            elif choices.lower() == 'h':
                local_help()
            if choices.isdigit():
                if int(choices) in check_num:
                    menuItems[list(menuItems.keys())[int(choices)]]()
                else:
                    input('Oops!  That was no valid option. Try again...')
                    main()
            else:
                input('Oops!  That was no valid option. Try again...')
                main()
        else:
            print()
            print(colorize('BAD FILE -->','red'),colorize(filename,'red'))
            input('Press any key to exit')
            exit()


if __name__ == "__main__":
    main()

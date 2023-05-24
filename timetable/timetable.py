import csv, os
import re

def join_strings(list):
    str = ""
    for item in list:
        str += item + " "
    return str


def clean_list(list):
    new_list = []
    for item in list:
        if not re.search("^[; ]*$", item) and re.search("([A-Z0-1]{1}[0-9]{2})+", item[:3]):
            new_list.append(item.split(";"))
    return new_list


def horario_dict(list):
    turnos = ['DC', 'DS', 'CH', 'Fer', 'TA', 'MA', 'MB', 'NA', 'Fr', 'Fe', 'TE', 'MC', 'MR', 'MS', 'ME', 'NB', 'NBc', 'TB',
              'CGS', 'Do', 'MPp', 'FIn', 'FEx', 'AS', 'FAS', 'X']
    dict = {}
    mec = ''
    for item in list:
        for i in item:
            if re.search("([0-9]{5})", i):
                l = i.split()
                mec = l[1]
                dict[int(mec)] = []
            if mec != '' and [x for x in turnos if x in i] and i != '' and not re.search("([A-Z0-1]{1}[0-9]{2})+",
                                                                                         i[:3]):
                dict[int(mec)].append(i)

    return dict


def timetable(dict, size):
    noite = ['NA', 'NBc']
    manha = ['MA', 'MC', 'MR']
    tarde = ['TA']
    reab = ['TB']
    timetable = {}
    enf_reab = {}
    for i in range(size):
        timetable['N' + str(i + 1)] = []
        timetable['M' + str(i + 1)] = []
        timetable['T' + str(i + 1)] = []
        enf_reab['T' + str(i + 1)] = []

    for el in timetable.keys():
        for mec in dict.keys():
            n = int(el[1:]) - 1
            turnos = dict[mec]
            if el[:1] == "N":
                for item in noite:
                    if item in turnos[n]:
                        timetable[el].append(mec)
            if el[:1] == "M":
                for item in manha:
                    if item in turnos[n]:
                        timetable[el].append(mec)
            if el[:1] == "T":
                for item in tarde:
                    if item in turnos[n]:
                        timetable[el].append(mec)
                for item in reab:
                    if item in turnos[n]:
                        enf_reab[el].append(mec)

    return timetable, enf_reab


def size(dict):
    length = 0
    for item in dict.keys():
        if length == 0:
            length = len(dict[item])
        else:
            if length == len(dict[item]):
                continue
            else:
                print("Error - Size don't match in all workers")
        return length

horario = {}

def timetableClean(filename, output):
    list = []
    path = os.path.dirname(filename)
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            list.append(join_strings(row))

    c_list = clean_list(list)
    dict = {k: v for k, v in horario_dict(c_list).items() if v}
    horario, horario_reab = timetable(dict, size(dict))

    with open(path+'/'+output+'.txt', 'w') as convert_file:
        for key in horario.keys():
            convert_file.write("'{}':'{}'\n".format(key, horario[key]))
        convert_file.write("\n")
        for key in horario_reab.keys():
            convert_file.write("'{}':'{}'\n".format(key, horario_reab[key]))
        print(f'file created sucessfuly at {path}/{output}.txt')

        return horario, horario_reab
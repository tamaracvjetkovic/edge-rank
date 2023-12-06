
from parse_files import load_pickle_data
from edge_rank import calculate_edge_rank
from trie import Trie
from copy import deepcopy

import re
from termcolor import colored
from trie import Trie
import networkx as nx   


korisnik = ""
users = nx.DiGraph()
allStatuses = {}
usersStatuses = {}
statusesWeight = {}
trie = Trie()


def pretraga_fraze(s, topStatuses):
    global korisnik, users, allStatuses, statusesWeight, trie 
    print("\n")
    cnt = 0
    s = s.replace('"', "")
    s = s.strip()
    s2 = deepcopy(s)
    s2 = s2.lower()
    br = 0 
    dummy = s2
    dummyOK = 0
    for status in topStatuses:
        if (br == 10):
            break
        message = allStatuses[status[0]]["status_message"]
        m = deepcopy(message)
        m = m.lower()
        indexes = [m.start() for m in re.finditer(s2, m)]
        if (len(indexes) != 0):
            valids = []
            mes = deepcopy(message)
            mes = mes.lower()
            for i in indexes:
                if (i > 0 and ord(mes[i - 1]) != 32):
                    break
                elif (ord(mes[i + len(s)]) >= 97 and ord(mes[i + len(s)]) <= 122):
                    if (dummyOK == 1):
                        break
                    for j in range(i + len(s), len(mes)):
                        if (ord(mes[j]) >= 97 and ord(mes[j]) <= 122):
                            dummy += mes[j]
                            dummyOK = 1
                        else:
                            break
                    break
                else:
                    valids.append(i)
            if (len(valids) == 0):
                continue        
            print("\n", br + 1, end = "")
            br += 1
            print(". ", end = "")
            print(allStatuses[status[0]]["status_link"], " (", allStatuses[status[0]]["status_type"], ")\n")
            used = {}
            for i in valids:
                used[i] = 1
            pos = 0
            while (pos < len(message)):
                if pos in used:
                    st = ""
                    pos2 = pos
                    while (pos2 < pos + len(s2)):
                        st += message[pos2]
                        pos2 += 1
                    print(colored(st, "yellow"), end = "")
                    pos = pos2
                    continue    
                else:
                    print(message[pos], end = "")
                    pos += 1                     
            print("\n\nAUTHOR: ", allStatuses[status[0]]["author"])
            print("PUBLISHED: ", allStatuses[status[0]]["status_published"], "\n")
            if (int(allStatuses[status[0]]["num_likes"]) > 0):
                print("👍:", allStatuses[status[0]]["num_likes"], end = " | ")
            if (int(allStatuses[status[0]]["num_loves"]) > 0):
                print("❤️️ :", allStatuses[status[0]]["num_loves"], end = " | ")
            if (int(allStatuses[status[0]]["num_wows"]) > 0):
                print("😲:", allStatuses[status[0]]["num_wows"], end = " | ")
            if (int(allStatuses[status[0]]["num_hahas"]) > 0):
                print("😂:", allStatuses[status[0]]["num_hahas"], end = " | ")
            if (int(allStatuses[status[0]]["num_sads"]) > 0):
                print("😢:", allStatuses[status[0]]["num_sads"], end = " | ")
            if (int(allStatuses[status[0]]["num_angrys"]) > 0):
                print("😡:", allStatuses[status[0]]["num_angrys"], end = " | ")
            print("\n")
            if (int(allStatuses[status[0]]["num_comments"]) > 0):
                print(allStatuses[status[0]]["num_comments"], "comments..", end = "  ")
            if (int(allStatuses[status[0]]["num_shares"]) > 0):
                print(allStatuses[status[0]]["num_shares"], "shares..")   
            print("\n\n") 
            cnt += 1
    if (cnt == 0):
        print("\nNEMA REZULTATA PRETRAGE!\n")
        print('Da li ste možda mislili "', end = '')
        print(colored(dummy, "yellow", attrs = ["bold"]), end = '')
        print('"?\n')
    pretraga_meni(topStatuses)
    return


def pretraga_autocomplete(s, topStatuses):
    global korisnik, users, allStatuses, statusesWeight, trie 
    s = s.lower()
    s = s.strip()
    s = s.replace("*", "")
    res = []
    used = {}
    for status in topStatuses:
        words2 = allStatuses[status[0]]["status_message"]
        allWords = words2.split(" ")
        for word in allWords:
            word2 = deepcopy(word)
            word2 = word2.lower()
            st = ""
            ok = 1
            for letter in word:
                l = letter.lower()
                if (ord(l) < 97 or ord(l) > 122):
                    if (ord(letter) == 39):
                        break
                    else:
                        if (st != ""):
                            res.append(st)
                        ok = 0
                        st = ""
                        continue
                st += letter
            if (ok == 1):
                if (word != ""):
                    res.append(word)   
            else:  
                if (st != ""):
                    res.append(st)
    result = []
    for word in res:
        word2 = deepcopy(word)
        word2 = word2.lower()
        s2 = deepcopy(s)
        s2 = s2.lower()
        if (word2.startswith(s2)):
            checking = 1
            for w in word2:
                if (ord(w) >= 97 and ord(w) <= 122):
                    continue
                else:
                    checking = 0
            if checking == 0:
                continue
            if (len(result) > 3):
                break
            if word2 in used:
                continue
            used[word2] = 1
            result.append(word2) 
    print("\n\nRezultat: ", end = "")
    for i in range(0, len(result)):
        if i == len(result) - 1:
            pass
            print(result[i], end = "\n\n")
        else:
            pass
            print(result[i], end = ", ")
    s = input("\nUnesite tekst: ")
    print("\n")
    brApo = 0
    brStars = 0
    spaces = 0
    br = 0
    for l in s:
        l = l.lower()
        if (l == '"'):
            brApo += 1
            continue
        elif (l == '*'):
            brStars += 1
            continue
        elif (l == " "):
            spaces += 1
            continue
        elif (ord(l) >= 97 and ord(l) <= 122):
            continue
        else:
            br += 1   
    if (brApo == 2 and s[0] == '"' and s[len(s) - 1] == '"'):
        pretraga_fraze(s, topStatuses)
        return
    elif (spaces == 0 and brStars == 1 and s[len(s) - 1] == '*'):
        pretraga_autocomplete(s, topStatuses)
        return
    elif (br > 0 or brApo > 2 or brStars > 1):
        pretraga_meni(topStatuses)
        return
    else:
        pretraga_objava(s, topStatuses)
        return
    

def pretraga_objava(s, topStatuses):
    global korisnik, users, allStatuses, statusesWeight, trie 
    print("\n")
    s = s.strip()
    if (s == ""):
        pregled_objava(topStatuses)
        pretraga_meni(topStatuses)
        return
    show = {}
    res2 = trie.search(s)    
    keysRes = list(res2.keys())
    pr = ""
    while(pr in keysRes):
        keysRes.remove(pr)
    stWeight = deepcopy(statusesWeights)
    for key in keysRes:
        dict = res2[key][1]
        for key in stWeight:
            if key in dict:
                show[key] = 1
                stWeight[key] *= (10000000 * dict[key])
                
    sortedStatuses = sorted(stWeight.items(), key = lambda x : round(float(x[1]), 3), reverse = True)
    cnt = 0    
    for i in range(0, len(sortedStatuses)):
        if (cnt == 10):
            break
        st = sortedStatuses[i]
        statusKey = st[0]
        if statusKey not in show:
            continue     
        cnt += 1
        print("\n", i + 1, end = "")
        print(". ", end = "")
        print(allStatuses[statusKey]["status_link"], " (", allStatuses[statusKey]["status_type"], ")\n")
        message = allStatuses[statusKey]["status_message"]
        m = deepcopy(message)
        m = m.lower()
        allIndexes = {}
        for key in keysRes:
            indexes = [m.start() for m in re.finditer(key, m)]
            for ind in indexes:         # Sarina Hudgens 
                allIndexes[ind] = key   # breaking BREAKING cnn CNN cnn Bill Trump Hillary as
        pos = 0
        while (pos < len(message)):
            if pos in allIndexes:
                if (pos > 0):
                    l = message[pos - 1].lower()
                    if (ord(l) >= 97 and ord(l) <= 122):
                        print(message[pos], end = "")
                        pos += 1 
                        continue
                pos2 = pos
                st = ""
                while (pos2 < pos + len(allIndexes[pos])):
                    st += message[pos2]
                    pos2 += 1
                if (pos2 < len(message) - 1):
                    l = message[pos2].lower()
                    if (ord(l) >= 97 and ord(l) <= 122):
                        print(st, end = "")
                        pos = pos2
                        continue
                print(colored(st, "yellow"), end = "")
                pos = pos2
                continue    
            else:
                print(message[pos], end = "")
                pos += 1                     
        print("\n\nAUTHOR: ", allStatuses[statusKey]["author"])
        print("PUBLISHED: ", allStatuses[statusKey]["status_published"], "\n")
        if (int(allStatuses[statusKey]["num_likes"]) > 0):
            print("👍:", allStatuses[statusKey]["num_likes"], end = " | ")
        if (int(allStatuses[statusKey]["num_loves"]) > 0):
            print("❤️ :", allStatuses[statusKey]["num_loves"], end = " | ")
        if (int(allStatuses[statusKey]["num_wows"]) > 0):
            print("😲:", allStatuses[statusKey]["num_wows"], end = " | ")
        if (int(allStatuses[statusKey]["num_hahas"]) > 0):
            print("😂:", allStatuses[statusKey]["num_hahas"], end = " | ")
        if (int(allStatuses[statusKey]["num_sads"]) > 0):
            print("😢:", allStatuses[statusKey]["num_sads"], end = " | ")
        if (int(allStatuses[statusKey]["num_angrys"]) > 0):
            print("😡:", allStatuses[statusKey]["num_angrys"], end = " | ")
        print("\n")
        if (int(allStatuses[statusKey]["num_comments"]) > 0):
            print(allStatuses[statusKey]["num_comments"], "comments..", end = "  ")
        if (int(allStatuses[statusKey]["num_shares"]) > 0):
            print(allStatuses[statusKey]["num_shares"], "shares..")   
        print("\n\n") 
    if (cnt == 0):
        print("\nNEMA REZULTATA PRETRAGE!\n")  
    pretraga_meni(topStatuses)
    return


def pretraga_meni(topStatuses): 
    global korisnik, users, allStatuses, statusesWeight, trie 
    s = input("\n\nPRETRAGA:\nUnesite tekst: ")
    brApo = 0
    brStars = 0
    spaces = 0
    br = 0
    for l in s:
        l = l.lower()
        if (l == '"'):
            brApo += 1
            continue
        elif (l == '*'):
            brStars += 1
            continue
        elif (l == " "):
            spaces += 1
            continue
        elif (ord(l) >= 97 and ord(l) <= 122):
            continue
        else:
            br += 1   
    if (brApo == 2 and s[0] == '"' and s[len(s) - 1] == '"'):
        if (len(s) == 2):
            pretraga_meni(topStatuses)
            return
        pretraga_fraze(s, topStatuses)
    elif (spaces == 0 and brStars == 1 and s[len(s) - 1] == '*'):
        if (len(s) == 1):
            pretraga_meni(topStatuses)
            return
        pretraga_autocomplete(s, topStatuses)
    elif (br > 0 or brApo > 2 or brStars > 1 or brApo == 1):
        pretraga_meni(topStatuses)
        return
    else:
        pretraga_objava(s, topStatuses)


def pregled_objava(topStatuses):
    global korisnik, users, allStatuses, statusesWeight, trie 
    print("\n")
    cnt = 0
    for i in range(0, min(10, len(topStatuses))):
        cnt += 1
        st = topStatuses[i]
        statusKey = st[0]
        print("\n", i + 1, end = "")
        print(". ", end = "")
        print(allStatuses[statusKey]["status_link"], " (", allStatuses[statusKey]["status_type"], ")\n")
        print(allStatuses[statusKey]["status_message"], "\n")
        print("AUTHOR: ", allStatuses[statusKey]["author"])
        print("PUBLISHED: ", allStatuses[statusKey]["status_published"], "\n")
        if (int(allStatuses[statusKey]["num_likes"]) > 0):
            print("👍:", allStatuses[statusKey]["num_likes"], end = " | ")
        if (int(allStatuses[statusKey]["num_loves"]) > 0):
            print("❤️️ :", allStatuses[statusKey]["num_loves"], end = " | ")
        if (int(allStatuses[statusKey]["num_wows"]) > 0):
            print("😲:", allStatuses[statusKey]["num_wows"], end = " | ")
        if (int(allStatuses[statusKey]["num_hahas"]) > 0):
            print("😂:", allStatuses[statusKey]["num_hahas"], end = " | ")
        if (int(allStatuses[statusKey]["num_sads"]) > 0):
            print("😢:", allStatuses[statusKey]["num_sads"], end = " | ")
        if (int(allStatuses[statusKey]["num_angrys"]) > 0):
            print("😡:", allStatuses[statusKey]["num_angrys"], end = " | ")
        print("\n")
        if (int(allStatuses[statusKey]["num_comments"]) > 0):
            print(allStatuses[statusKey]["num_comments"], "comments..", end = "  ")
        if (int(allStatuses[statusKey]["num_shares"]) > 0):
            print(allStatuses[statusKey]["num_shares"], "shares..")   
        print("\n\n") 
    if (cnt == 0):
        print("\nNEMA OBJAVA!\n")


def glavni_meni():
    global korisnik, users, allStatuses, statusesWeight, trie 
    while (True):
        topStatuses = calculate_edge_rank(users, allStatuses, statusesWeights, korisnik) 
        pregled_objava(topStatuses)
        pretraga_meni(topStatuses)
        
        

if __name__ == '__main__':
        

    print("\n\nAplikacija se očitava..\n\n")
    users, allStatuses, statusesWeights, trie = load_pickle_data()
    
    print("\nDOBRODOŠLI!\n\n")
    korisnik = ""
    while (True):
        print("\n(npr. Ed Black)")
        imePrezime = input("\nUnesite ime i prezime: ")
        if (imePrezime in users):
            korisnik = imePrezime
            print("\n")
            break 
    
    glavni_meni()  
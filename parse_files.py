
from random import randint, random
from datetime import datetime, timedelta

from edge_rank import calculate_statuses_weight, calculate_comments_weight, calculate_shares_weight, calculate_reactions_weight
from trie import Trie
import networkx as nx

import time
import pickle


users = nx.DiGraph()
allStatuses = {}
statusesWeight = {}
trie = Trie()
g = 0


def load_friends(path):
    global users, g
    g = 1
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        for index in range(1, len(lines)):
            line = lines[index]
            line = line.strip()
            data = line.split(",")
            n = len(data)
            user = str(data[0])
            for j in range(2, n):
                friendName = data[j]
                users.add_edge(user, friendName, weight = 15000)  


def load_statuses(path):
    extracted_statuses = []
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        comment = ""
        paired_ellipses = True
        for index in range(1, len(lines)):
            line = lines[index]
            if line == "\n":
                comment += line
                continue
            line = line.strip()
            previous_index = -1
            while True:
                index = line.index("\"", previous_index+1) if "\"" in line[previous_index+1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index
            comment += line
            if not paired_ellipses:
                continue
            data = comment.split(",")
            n = len(data)     
            if n < 16:
                raise Exception("Status does not contain necessary data.")
            elif n > 16:
                comment_text = "".join(data[1:n-14])
            else:
                comment_text = data[1]           
            extracted_statuses.append([data[0], comment_text, data[n-14], data[n-13], data[n-12], data[n-11],
                             data[n-10], data[n-9], data[n-8], data[n-7], data[n-6], data[n-5], data[n-4],
                             data[n-3], data[n-2], data[n-1]])
            comment = ""
            paired_ellipses = True  
    return extracted_statuses
def load_statuses2(path, now):
    global allStatuses, statusesWeight
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        comment = ""
        paired_ellipses = True
        for index in range(1, len(lines)):
            line = lines[index]
            if line == "\n":
                comment += line
                continue
            line = line.strip()
            previous_index = -1
            while True:
                index = line.index("\"", previous_index+1) if "\"" in line[previous_index+1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index
            comment += line
            if not paired_ellipses:
                continue
            data = comment.split(",")
            n = len(data)     
            if n < 16:
                raise Exception("Status does not contain necessary data.")
            elif n > 16:
                comment_text = "".join(data[1:n-14])
            else:
                comment_text = data[1]           
            comment = ""
            paired_ellipses = True
            allStatuses2, statusesWeight2 = calculate_statuses_weight(data, comment_text, allStatuses, statusesWeight, now)   
            allStatuses = allStatuses2 
            statusesWeight = statusesWeight2     
            

def load_comments(path):
    output_data = []
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False
        for index in range(1, len(lines)):
            line = lines[index]
            if line == "\n":
                comment += line
            if line[-1] == "\n":
                line = line[:-1]
            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True
            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True
            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line
            data = comment.split(",")
            n = len(data)
            if n < 14:
                raise Exception("Comment does not contain necessary data.")
            elif n > 14:
                comment_text = "".join(data[3:n - 10])
            else:
                comment_text = data[3]
                
            content = [data[0], data[1], data[2], comment_text, data[n - 10], data[n - 9], data[n - 8], data[n - 7],
                       data[n - 6], data[n - 5], data[n - 4], data[n - 3], data[n - 2], data[n - 1]]
            output_data.append(content)
            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data
def load_comments2(path, now):
    global allStatuses, users
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False
        for index in range(1, len(lines)):
            line = lines[index]
            if line == "\n":
                comment += line
            if line[-1] == "\n":
                line = line[:-1]
            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True
            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True
            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line
            data = comment.split(",")
            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
            users2 = calculate_comments_weight(data, allStatuses, users, now)
            users = users2


def load_shares(path):
    shares = []
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            shares.append(data)
    return shares
def load_shares2(path, now):
    global users, allStatuses
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            users2 = calculate_shares_weight(data, allStatuses, users, now)
            users = users2

def load_reactions(path):
    reactions = []
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            reactions.append(data)
    return reactions
def load_reactions2(path, now):
    global users, allStatuses
    with open(path, encoding = 'utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            users2 = calculate_reactions_weight(data, allStatuses, users, now)
            users = users2
            
def load_trie():
    global trie, allStatuses
    for status in allStatuses:
        words2 = allStatuses[status]["status_message"]
        allWords = words2.split(" ")
        for word in allWords:
            st = ""
            ok = 1
            for letter in word:
                l = letter.lower()
                if (ord(l) < 97 or ord(l) > 122):
                    if (ord(letter) == 39):
                        break
                    else:
                        if (st != ""):
                            trie.insert(st, status)
                        ok = 0
                        st = ""
                        continue
                st += letter
            if (ok == 1):
                if (word != ""):
                    trie.insert(word, status)    
            else:  
                if (st != ""):
                    trie.insert(st, status)           
       

def get_statuses_header():
    return ",".join(["status_id", "status_message", "status_type", "status_link",
                     "status_published", "author", "num_reactions", "num_comments", "num_shares",
                     "num_likes", "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys",
                     "num_special"])

def get_reaction_header():
    return "status_id,type_of_reaction,reactor,reacted"

def get_share_header():
    return "status_id,sharer,status_shared"

def get_comment_header():
    return "comment_id,status_id,parent_id,comment_message,comment_author,comment_published,num_reactions,num_likes," \
           "num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special"
           


def generate_datetime_after_datetime(date_str):
    format_str = "%Y-%m-%d %H:%M:%S"
    start_datetime = time.strptime(date_str, format_str)
    end_datetime = time.localtime(time.time())

    start_time = time.mktime(start_datetime)
    end_time = time.mktime(end_datetime)

    ptime = start_time + random() * (end_time - start_time)
    return time.strftime(format_str, time.localtime(ptime))


def modify_date_to_recent(date_str):
    format_str = "%Y-%m-%d %H:%M:%S"
    old_date = datetime.strptime(date_str, format_str)

    days_ago = [_ for _ in range(30)]
    days_ago.extend(_ for _ in range(0, 16))
    days_ago.extend(_ for _ in range(0, 6))
    days_ago.extend(_ for _ in range(0, 2))

    rand_num = days_ago[randint(0, len(days_ago)-1)]
    generated_date = datetime.today() - timedelta(days=rand_num)

    new_date = old_date.replace(year=generated_date.year, month=generated_date.month, day=generated_date.day)
    return str(new_date)


def load_all(statuses_path, comments_path, shares_path, reactions_path, ok):
    now = datetime.now() + timedelta(days = 1)
    if (ok == 0):
        print("  Loading friends...")
        start = time.time()
        load_friends("dataset/friends.csv")
        end = time.time()
        print("  ✓ LOADED FRIENDS. Time elapsed: ", round((end - start), 4), "s\n")
    if (ok == 1):
        print("  Adding statuses...")
    else:    
        print("  Loading statuses...")
    start = time.time()
    load_statuses2(statuses_path, now)
    end = time.time()
    if (ok == 1):
        print("  ✓ ADDED STATUSES. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Adding comments...")
    else:    
        print("  ✓ LOADED STATUSES. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Loading comments...")
    start = time.time()
    load_comments2(comments_path, now)
    end = time.time()
    if (ok == 1):
        print("  ✓ ADDED COMMENTS. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Adding shares...")
    else:    
        print("  ✓ LOADED COMMENTS. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Loading shares...")
    start = time.time()
    load_shares2(shares_path, now)
    end = time.time()
    if (ok == 1):
        print("  ✓ ADDED SHARES. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Adding reactions...")
    else:    
        print("  ✓ LOADED SHARES. Time elapsed: ", round((end - start), 4), "s\n")
        print("  Loading reactions...")
    start = time.time()
    load_reactions2(reactions_path, now)
    end = time.time()
    if (ok == 1):
        print("  ✓ ADDED REACTIONS. Time elapsed: ", round((end - start), 4), "s\n")
    else:    
        print("  ✓ LOADED REACTIONS. Time elapsed: ", round((end - start), 4), "s\n")
    if (ok == 1):
        print("  Generating Trie...")
        start = time.time()
        load_trie()
        end = time.time()
        print("  ✓ GENERATED TRIE. Time elapsed: ", round((end - start), 4), "s\n")
    

def adjust_date_time(statuses_path, comments_path, shares_path, reactions_path):
    '''
    Podešava datume test objava na datume u poslednjih mesec dana (sa većom verovatnoćom da su
    bliži današnjem datumu). U skladu sa tim, ažurira i datume komentara, deljenja i reakcija.
    :param statuses_path: putanja do fajla sa statusima
    :param comments_path: putanja do fajla sa komentarima
    :param shares_path: putanja do fajla sa deljenjima
    :param reactions_path: putanja do fajla sa reakcijama
    '''
    statuses = load_statuses(statuses_path)
    status_to_datetime = {}
    with open(statuses_path, "w", encoding = 'utf-8') as file:
        file.write(get_statuses_header()+"\n")
        for status in statuses:
            status_datetime = status[4]
            new_status_datetime = modify_date_to_recent(status_datetime)
            status_to_datetime[status[0].strip()] = new_status_datetime
            status[4] = new_status_datetime       
            file.write(",".join(status) + "\n")

    comments = load_comments(comments_path)
    with open(comments_path, "w", encoding = 'utf-8') as file:
        file.write(get_comment_header() + "\n")
        for comment in comments:
            comment[5] = generate_datetime_after_datetime(status_to_datetime[comment[1]])
            file.write(",".join(comment) + "\n")

    shares = load_shares(shares_path)
    with open(shares_path, "w", encoding = 'utf-8') as file:
        file.write(get_share_header() + "\n")
        for share in shares:
            share[2] = generate_datetime_after_datetime(status_to_datetime[share[0]])
            file.write(",".join(share) + "\n")

    reactions = load_reactions(reactions_path)
    with open(reactions_path, "w", encoding = 'utf-8') as file:
        file.write(get_reaction_header() + "\n")
        for reaction in reactions:
            reaction[3] = generate_datetime_after_datetime(status_to_datetime[reaction[0]])
            file.write(",".join(reaction) + "\n")


def save_pickle_data():
    global users, allStatuses, statusesWeight, trie
    usersPickle = pickle.dumps(users)
    with open('saved_data/users.csv', 'wb') as file:
        file.write(usersPickle) 
    statusesPickle = pickle.dumps(allStatuses)
    with open('saved_data/statuses.csv', 'wb') as file:
        file.write(statusesPickle)     
    statusesWeightPickle = pickle.dumps(statusesWeight)
    with open('saved_data/statuses_weight.csv', 'wb') as file:
        file.write(statusesWeightPickle)    
    triePickle = pickle.dumps(trie)
    with open('saved_data/trie.csv', 'wb') as file:
        file.write(triePickle)

def load_pickle_data():
    with open('saved_data/users.csv', 'rb') as file:
        loaded_users = pickle.load(file)  
    with open('saved_data/statuses.csv', 'rb') as file:
        loaded_statuses = pickle.load(file)    
    with open('saved_data/statuses_weight.csv', 'rb') as file:
        loaded_statuses_weight = pickle.load(file)
    with open('saved_data/trie.csv', 'rb') as file:
        loaded_trie = pickle.load(file)
    return loaded_users, loaded_statuses, loaded_statuses_weight, loaded_trie



def add_original_files():
    print("\n\nAdjusting datetime in original files...")
    start = time.time()
    adjust_date_time("dataset/original_statuses.csv", "dataset/original_comments.csv", "dataset/original_shares.csv", "dataset/original_reactions.csv")
    end = time.time()
    print("✓ ADJUSTED DATES. Time elapsed: ", round((end - start), 4), "s\n\n")
    
    print("Loading data from original files...\n")
    start = time.time()
    load_all("dataset/original_statuses.csv", "dataset/original_comments.csv", "dataset/original_shares.csv", "dataset/original_reactions.csv", 0)
    end = time.time()
    print("\n✓ LOADED DATA. Time elapsed: ", round((end - start), 4), "s\n\n")

    
def add_test_files():
    global users, allStatuses, statusesWeight, trie
     
    print("\n\nAdjusting datetime in test files...")
    start = time.time()
    adjust_date_time("dataset/test_statuses.csv", "dataset/test_comments.csv", "dataset/test_shares.csv", "dataset/test_reactions.csv")
    end = time.time()
    print("✓ ADJUSTED DATES. Time elapsed: ", round((end - start), 4), "s\n\n")
    
    print("Loading all data from original files...")
    start = time.time()
    users, allStatuses, statusesWeight, trie = load_pickle_data()
    end = time.time()
    print("✓ LOADED DATA. Time elapsed: ", round((end - start), 4), "s\n\n")
    
    print("Adding data from test files...\n")
    start = time.time()
    load_all("dataset/test_statuses.csv", "dataset/test_comments.csv", "dataset/test_shares.csv", "dataset/test_reactions.csv", 1)
    end = time.time()
    print("\n✓ ADDED DATA. Time elapsed: ", round((end - start), 4), "s\n\n")


def set_everything():
    
    add_original_files()
    add_test_files()
    
    print("Saving all data...")
    start = time.time()
    save_pickle_data()
    end = time.time()
    print("✓ SAVED DATA. Time elapsed: ", round((end - start), 4), "s\n\n")
    
    print("\n\nALL DONE!\n\n\n")
    
    
    
if __name__ == '__main__':
    #pass
    set_everything()
    
    

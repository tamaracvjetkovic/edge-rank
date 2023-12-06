
from datetime import datetime



def calculate_edge_rank(users, statuses, statusesWeight, korisnik):
    allStatuses = []
    myDict = {}
    for statusKey in statuses:
        statusValue =  statusesWeight[statusKey]
        autor = statuses[statusKey]["author"]
        if (autor in users[korisnik]):
            statusValue *= users[korisnik][autor]['weight']
        statusValue = round(statusValue, 3)
        myDict[statusKey] = float(statusValue)
        allStatuses.append({"value":round(statusValue, 3), "status_key":statusKey})
    sortedStatuses = sorted(myDict.items(), key = lambda x : round(float(x[1]), 3), reverse = True)
    return sortedStatuses

    
def calculate_statuses_weight(data, comment_text, statuses, statusesWeight, now):
    statusKey = str(data[0])
    n = len(data) 
    statuses[statusKey] = {"status_message": comment_text,
                            "status_type": data[n - 14],
                            "status_link": data[n - 13],
                            "status_published": data[n - 12],
                            "author": data[n - 11],
                            "num_comments": int(data[n - 10]),
                            "num_shares": int(data[n - 9]),
                            "num_likes": int(data[n - 8]),
                            "num_loves": int(data[n - 7]),
                            "num_wows": int(data[n - 6]),
                            "num_hahas": int(data[n - 5]),
                            "num_sads": int(data[n - 4]),
                            "num_angrys": int(data[n - 3]),
                            "num_special": int(data[n - 2]),
                            }
    statusesWeight[statusKey] = 0
    tip = 1000;
    if (data[n - 14] == "photo"):
        tip = 3000
    if (data[n - 14] == "video"):
        tip = 5000
    com = int(data[n - 10]) * 20
    share = int(data[n - 9]) * 30
    like = int(data[n - 8]) * 10
    w =  float((tip + com + share + like + int(data[n - 7]) +  int(data[n - 6]) + int(data[n - 5]) + int(data[n - 4]) + int(data[n - 3]) + int(data[n - 2])))
    date_format = "%Y-%m-%d %H:%M:%S"
    datum = datetime.strptime(data[n - 12], date_format) 
    seconds = (now - datum).total_seconds()
    p = float((10000000000000 / seconds))
    statusesWeight[statusKey] =  float(w + p)
    return statuses, statusesWeight


def calculate_comments_weight(data, statuses, users, now):
    statusKey = data[1]
    autorName = statuses[statusKey]["author"]
    tip = 1
    if (data[2] != ""):
        tip = 2
    komentarisao = data[4]
    date_format = "%Y-%m-%d %H:%M:%S"
    datum = datetime.strptime(data[5], date_format) 
    seconds = (now - datum).total_seconds()
    w =  float(4500 * float((10 / seconds)))
    if (tip == 2):
        w *= 2
    if autorName in users[komentarisao]:
        users[komentarisao][autorName]['weight'] += w
    else:
        users.add_edge(komentarisao, autorName, weight = w) 
    return users


def calculate_shares_weight(data, statuses, users, now):
    statusKey = data[0]
    autorName = statuses[statusKey]["author"]
    sherovao = data[1]
    date_format = "%Y-%m-%d %H:%M:%S"
    datum = datetime.strptime(data[2], date_format) 
    seconds = (now - datum).total_seconds()
    w =  float(6000 * float((10 / seconds)))
    if autorName in users[sherovao]:    
        users[sherovao][autorName]['weight'] += w
    else:
        users.add_edge(sherovao, autorName, weight = w)     
    return users


def calculate_reactions_weight(data, statuses, users, now):
    statusKey = data[0]
    autorName = statuses[statusKey]["author"]
    tip = data[1]
    reaktovao = data[2]
    date_format = "%Y-%m-%d %H:%M:%S"
    datum = datetime.strptime(data[3], date_format) 
    seconds = (now - datum).total_seconds()
    w = float(1000 * float((10 / seconds)))
    if (tip == "likes"):
        w =  float(2000 * float((10 / seconds)))
    if autorName in users[reaktovao]:
        users[reaktovao][autorName]['weight'] += w
    else:
        users.add_edge(reaktovao, autorName, weight = w)    
    return users

class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = []
        self.kraj = False
        self.cnt = 0
        self.statusesKeys = {}
        
        
class Trie:
    def __init__(self):
        self.root = TrieNode('')
        
    def insert(self, word2, statusKey):
        word = word2.lower()
        node = self.root
        for char in word:
            found = False
            for child in node.children:
                if child.char == char:
                    found = True
                    node = child
                    break
            if not found:
                newNode = TrieNode(char)
                node.children.append(newNode)
                node = newNode
        node.kraj = True
        if statusKey in node.statusesKeys:
            node.statusesKeys[statusKey] += 1
        else:
            node.statusesKeys[statusKey] = 1
    
    
    def search(self, string):
        if (len(string) == 0):
            return {}
        if (string[0] == '"'):
            return (self.search_phrases(string))
        return (self.search_words(string))


    def search_words(self, words2):
        words2 = words2.lower()
        words = words2.split(" ") 
        words = list(set(words))
        res = {}
        for word in words:
            for l in word:
                l = l.lower()
                if (ord(l) >= 97 and ord(l) <= 122):
                    continue
                else:
                    break
            (x, y) = self.search_word(word)
            res[word] = (x, y)    
        return res      
                 
    def search_word(self, word2):
        word = word2.lower()
        node = self.root
        for char in word:
            found = False
            for child in node.children:
                if child.char == char:
                    found = True
                    node = child
                    break
            if not found:
                return None, []
        return node.cnt, node.statusesKeys
    
    def search_phrases(self, phrase):
        pass
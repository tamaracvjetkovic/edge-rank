# EdgeRank 🌐

A console application for simulating the algorithm EdgeRank.

---

This was one of two university projects for the course "Algorithms and Data Structures", taken in the 2nd semester of the Software Engineering and Information Technologies program.

The ``goal`` of the project was to:
- simulate and implement the EdgeRank algorithm developed by Facebook and calculate scores for all posts,
- utilize Trie structure for optimized searching, serialization, and deserialization
#
Technologies used: 
- ``Python``
#
Date: June, 2023.

---

# How does it work? ❓
- shows the feed of the currently logged-in user (top 10 posts depending on the post scores),
- enables the search option for: 1) word/words, 2) phrases, and an option for autocompletion

---

# Visual Design ✨
![Screenshot](screenshot1.png)
![Screenshot](screenshot2.png)
![Screenshot](screenshot3.png)
# 

---

# Using the Application ⚙️

To use this application, follow the next steps:
1) clone this repo,
2) open the project in a Python IDE,
3) run the program (main.py)

> NOTE: *the data (for users and posts) was not commited (it was >150MB)

---

# Examples 💡

After logging in with name and surname, the person's feed will show up in console.

You have an option of search which is case-insensitive. There are three options of searching:
- ``word/words``
  - type in one word (e.g. "will" or "Obama") or more words (e.g. "should will I as")
  - you will get top 10 posts ranked by score and number of words in them  
- ``phrases``
  - you can type whole phrases, e.g. "Obama will do" and you will get posts that only contain the whole phrase in them
- ``autocomplete``
  - this action doesn't return posts, but autocompleted words that are popular (e.g. "wi*" will return "will, with, win..." depending on the popularity of the words)


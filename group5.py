import os

import re
from nltk.stem import PorterStemmer

import time
import pickle

PATH = "../HillaryEmails/"
porter = PorterStemmer()


# # # # # # TASK 0 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def listDir(directory):
    return os.listdir(directory)
    

def readFile(fname):
    f = open(fname,"r")
    filee = f.read()
    f.close()
    return filee

# # # # # # TASK 1 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PS: Some feaatures that shoukd be done in linguistic module is done here! 
# like lowercase and eliminating punctuations
def tokenization(filee):
    token_list = []
    lines = filee.strip().split("\n")
    for line in lines:
        tokens = re.split(r'\W+', line.strip())
        tokens = [t.lower() for t in tokens if len(t)>1]
        token_list.extend(tokens)
    return token_list
    
# # # # # # TASK 2 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
def linguistic(tokenDoc_pair):
    i=0
    while i<len(tokenDoc_pair):
        tokenDoc_pair[i][0] = porter.stem(tokenDoc_pair[i][0])
        i+=1
    
# # # # # # TASK 3 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
def sorting(tokenDoc_pair):
    tokenDoc_pair.sort()  
   
# # # # # # TASK 4 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   
def convert2postings(tokenDoc_pair):
    postings={}
    for i,tD in enumerate(tokenDoc_pair):
        if tD[0] not in postings.keys():
            postings[tD[0]] = [tD[1]]
        else:
            if tD[1] not in postings[tD[0]]:
                postings[tD[0]].append(tD[1])

    # Doc ids in the posting list are stored as id directly but wew might change
    # and store them as gaps.
    return postings
        
# # # # # # TASK 5 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #           
def merge(posting_lists):
    return    
    
    
    
    
# # # # # # TASK 6 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #      
def create_index(path):
    files = listDir(path)

    token_table = []
    for f in files:
        for t in tokenization(readFile(PATH + f)):
            token_table.append([t,f.strip().split(".")[0]])
        
    linguistic(token_table)    
    
    sorting(token_table)
    
    return convert2postings(token_table)

def query(u_query):
    token_table = []
    for t in tokenization(u_query):
        token_table.append([t,"query"])
    linguistic(token_table)
    result_postings_list = []    
    for t in token_table:
        result_postings_list.append(postings[t[0]])
    
    # The elements of this list named 'result_postings_list' should give the merge
    # and this function should find their overlap      
    
    
    return result_postings_list



if os.path.exists("postings.p"):
    print ("Index (Postings) loading ...") 
    start = time.clock()
    postings=pickle.load(open("postings.p","rb"))
    print ("Index loading time " + str(time.clock()-start))
else:    
    print("index (Postings) creating...")
    start = time.clock()
    postings = create_index(PATH)
    stop = time.clock()
    print("index creating time "+str(time.clock()-start))
    print("index created")    
    pickle.dump(postings,open("postings.p","wb"))
    print("And dumped")

if __name__ == "__main__":
    while True: 
        print("")
        user_query = input("Enter query ('q' to stop): ")
        if (user_query.strip().lower() == 'q'):
            break
        print('----------------------------------------')
        start = time.clock()
        query_res = query(user_query)
        print("query_time " + str(time.clock()-start)+'\n')
        print("Result: "+str(query_res))
        

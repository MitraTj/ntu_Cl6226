import os
import sys
import re
from nltk.stem import PorterStemmer

import time
import pickle

PATH = "/home/ali/Downloads/InfoRet_project/HillaryEmails/"
porter = PorterStemmer()


# # # # # # TASK 0 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def listDir(directory):
    return [PATH + s for s in os.listdir(directory)]

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
    tmp_time = time.clock()
    for i,tD in enumerate(tokenDoc_pair):
        ratio = float(i)/len(tokenDoc_pair)*100
        if ratio%5 == 0:
            print(str(ratio)+"% of tokens are converted to postings and it takes " + str(time.clock()-tmp_time)+ " seconds.")        
            tmp_time = time.clock()
#        if tD[0] not in postings.keys():
        if postings.get(tD[0]) == None:
            postings[tD[0]] = [tD[1]]
        else:
            if tD[1] not in postings[tD[0]]:
                postings[tD[0]].append(tD[1])

    # Doc ids in the posting list are stored as id directly but we might change
    # and store them as gaps.
    return postings
        
# # # # # # TASK 5 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
# function intersect is for finding intersection of two list in an efficient way
def intersect(p1,p2):
    intersect = []
    if len(p1) != 0 and len(p2) != 0:
        count1 = 0
        count2 = 0
        while count1<len(p1) and count2<len(p2):
            if p1[count1] == p2[count2]:
                intersect.append(p1[count1])
                count1 += 1
                count2 += 1
            elif p1[count1] < p2[count2]:
                count1 += 1
            else:
                count2 += 1
    return intersect
    
# The function merge is calling function intersect for each pair of posling lists                    
def merge(posting_lists):
    if len(posting_lists) == 1:
        merged = posting_lists[0]
    else:
        i=1
        merged =[]
        while i < len(posting_lists):
            if i == 1:
                merged = intersect(posting_lists[0],posting_lists[1])
            else:
                merged = intersect(merged,posting_lists[i])
            i+=1
    return merged

# selecting shortes posting lists and intersecting them earlier makes merge 
# operation faster
def merge_efficient(posting_lists):    
    posting_lists.sort(key=len)
    return merge(posting_lists)


    
# # # # # # TASK 6 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #      
def create_index(path):
    files = listDir(path)

    token_table = []
#    print(files)
    tmp_time = time.clock()
    for i,f in enumerate(files):
        ratio = float(i)/len(files)*100
        if ratio%5 == 0:
            print(str(ratio)+"% of files are loaded")
        for t in tokenization(readFile(f)):
#            token_table.append([t,f.strip().split(".")[0]])
            token_table.append([t,i])
    print("token table generation takes::: " + str(time.clock()-tmp_time) + " seconds. Now linguistics ...")   
    tmp_time = time.clock()
    linguistic(token_table)    
    print("linguistcs takes::: " + str(time.clock()-tmp_time)+" seconds. Now sorting ...")
    tmp_time = time.clock()
    sorting(token_table)
    print("sorting takes::: " + str(time.clock()-tmp_time)+" seconds. Now inverted index generation (convert to postings) ...")
    return convert2postings(token_table), files

def query(u_query):
    token_table = []
    for t in tokenization(u_query):
        token_table.append([t,"query"])
    linguistic(token_table)
    result_postings_list = []    
    for t in token_table:
        try:
            result_postings_list.append(postings[t[0]])
        except:
            result_postings_list.append([])
    
    # The elements of this list named 'result_postings_list' should give the merge
    # and this function should find their overlap      
    return merge(result_postings_list)
    #Merge or Merge_efficient can be used


if os.path.exists("postings.p") and os.path.exists("files.p"):
    print ("Index (Postings) loading ...") 
    start = time.clock()
    postings=pickle.load(open("postings.p","rb"))
    files=pickle.load(open("files.p","rb"))    
    print ("Index loading time " + str(time.clock()-start))
else:    
    print("index (Postings) creating...")
    start = time.clock()
    postings, files = create_index(PATH)
    stop = time.clock()
    print("index creating time "+str(time.clock()-start))
    print("index created")    
    pickle.dump(postings,open("postings.p","wb"))
    pickle.dump(files,open("files.p","wb"))
    print("And dumped")
print("Size of index "+str(sys.getsizeof(postings))+" bytes")

if __name__ == "__main__":
    while True: 
        print("")
        user_query = raw_input("Enter query ('q' to stop): ")
        if (user_query.strip().lower() == 'q'):
            break
        print('----------------------------------------')
        start = time.clock()
        query_res = query(user_query)
        res=[]
        for r in query_res:
            res.append(files[r])
        print("query_time " + str(time.clock()-start)+'\n')
        if len(query_res) == 0:
            print("There is no such document related to '"+user_query+"'")
        else:
            print("Doc/s related to '"+user_query+"':::: "+str(res))
        




    

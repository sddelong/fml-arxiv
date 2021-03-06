""" script to go through data already saved in a pkl file and create + save a label file for
a single user.  use after running GetTestData.py. usage:

python LabelData.py 

Then follow the prompts."""

import cPickle
from ArxivData import Paper
from ArxivData import PromptUser



#get users name
user_name = raw_input("Please enter your name (no spaces, should match the name given to getTestData.py)):")

#filename where data is stored
data_filename = "./" + user_name + "CustomTestData.pkl"

data_file = open(data_filename,"rb")


paper_list = cPickle.load(data_file)

print paper_list

#initialize list of labels
label_list = []

for paper in paper_list:
    print "-"*80
    label = PromptUser(paper)

    label_list.append(label)
    

out_file = open(str(user_name) + "customlabels.pkl","wb")
cPickle.dump(label_list,out_file)
    
    


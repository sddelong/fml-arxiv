from ArxivData import FeaturizeVector
import cPickle
from ArxivData import Paper
from ArxivData import PromptUser
from OnlineSVM import OnlineSVMClassifier
from Perceptron import PerceptronClassifier


#helper functions to set up classifiers
def makePerceptronClassifier(parameters):
    """ parameters are just eta """
    
    classifier = PerceptronClassifier(parameters[0])



#names of people who contributed labels
names = ["steven","sid","iantobasco","joey","manas","travis"]

#get data
data_filename = "./OfficialTestData.pkl"
data_file = open(data_filename,"rb")
paper_list = cPickel.load(data_file)
abstracts = GetAbstracts(paper_list)
abtract_vectors = FeaturizeAbstracts(abstracts)

classifer_list = [MakePerceptronClassifier, MakeOnlineSVMClassifier, MakeOnlineSVMClassifier]
parameters_list = [[0.3], [0.3, 0.2],[0.3,0.4]]

#go through all classifiers to test
for cln in range(len(classifier_list)):
    
    classifier = classifier_list[cln](parameters_list[cln])

    #go through labeled data.
    for name in names:
        #get labels
        label_filename = name + "labels.pkl"
        label_file = open(label_filename,"rb")
    
        
    
    




    

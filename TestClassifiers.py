from ArxivData import FeaturizeAbstracts
from ArxivData import GetAbstracts
import numpy as np
import cPickle
from ArxivData import Paper
from ArxivData import PromptUser
from OnlineSVM import OnlineSVMClassifier
from OnlineSVM import MakeOnlineSVMClassifier
from Perceptron import PerceptronClassifier
from Perceptron import MakePerceptronClassifier



#names of people who contributed labels
names = ["steven","sid","iantobasco","joey","manas","travis"]

#get data
data_filename = "./OfficialTestData.pkl"
data_file = open(data_filename,"rb")
paper_list = cPickle.load(data_file)
abstracts = GetAbstracts(paper_list)
abstract_vectors = FeaturizeAbstracts(abstracts)

classifier_list = [MakePerceptronClassifier, MakeOnlineSVMClassifier, MakeOnlineSVMClassifier]
parameters_list = [[0.3], [0.3, 0.2],[0.3,0.4]]

#go through all classifiers to test
for cln in range(len(classifier_list)):
    
    for p in [1.0, 0.1]:

        #create classifier
        classifier = classifier_list[cln](parameters_list[cln])
        
        print classifier
        print "P value is: ", p
        
        #go through labeled data a few times, 
        for name in names:
            #get labels
            label_filename = name + "labels.pkl"
            label_file = open(label_filename,"rb")
            labels = cPickle.load(label_file)

            n_wrong = 0
            n_right = 0
            for i in range(len(abstract_vectors)):
            
                x = abstract_vectors[i]
                y_hat = classifier.Predict(x)
                y = labels[i]
                if y == y_hat:
                    n_right += 1
                elif y_hat == 1:
                    #update on false positive, add one to n_wrong
                    n_wrong += 1
                    classifier.Update(x,y_hat,y)
                else:
                    #maybe update on false negative, depends on p.
                    k = np.random.binomial(p,1)
                    n_wrong += 1
                    if k == 1:
                        classifier.Update(x,y_hat,y)
                        

            print "User: ", name
            print "Accuracy: ", float(n_right)/float(n_wrong + n_right)

        print "-"*80
            
                    
                
        
        
    
        
    
    




    

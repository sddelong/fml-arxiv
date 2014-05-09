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

            #initialize counts for accuracy
            n_pos_right = 0
            n_precision_wrong = 0
            n_recall_wrong = 0
            for i in range(len(abstract_vectors)):
            
                x = abstract_vectors[i]
                y_hat = classifier.Predict(x)
                y = labels[i]
                if y == 1 and y_hat == 1:
                    n_pos_right += 1
                elif y == -1 and y_hat == -1:
                    #do nothing, doesn't count as positive correct
                    pass
                elif y_hat == 1:
                    #update on false positive, add one to n_wrong
                    n_precision_wrong += 1
                    classifier.Update(x,y_hat,y)
                else:
                    #maybe update on false negative, depends on p.
                    n_recall_wrong += 1
                    k = np.random.binomial(1,p)
                    if k == 1:
                        classifier.Update(x,y_hat,y)
                        

            print "User: ", name
            print "Total preferred papers: ", n_pos_right + n_recall_wrong
            if n_pos_right != 0:
                print "Recall: ", float(n_pos_right)/float(n_pos_right + n_recall_wrong)
                print "Precision: ", float(n_pos_right)/float(n_pos_right + n_precision_wrong)
            else:
                print "Recall: ", 0.0
                print "Precision: ", 0.0

        print "-"*80
            
                    
                
        
        
    
        
    
    




    

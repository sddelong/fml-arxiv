"""
Script that grabs arxiv papers matching two different strings and trains a perceptron classifier
using bag of words from the abstract to identify which of the subjects the article is on 
run with:

python TrainArxivBatch <string1> <string2>

"""

#from ArxivData import GetDatedPapers
from ArxivData import SearchPapers
from ArxivData import GetAbstracts

from sklearn.feature_extraction.text import TfidfVectorizer
from Perceptron import PerceptronClassifier
from Perceptron import KernelPerceptronClassifier
from Perceptron import DotKernel
import numpy as np
import sys


if __name__ == "__main__":


    #parameters
    n_negative = 10
    n_positive = 10
    
    #random permutation of indices, so 
    # the algorithm doesn't see data all positive then all negative
    idxs = np.random.permutation(n_negative + n_positive)

    #test positive results, Brownian Dynamics
    paper_list = SearchPapers(sys.argv[1],n_positive)
    abstracts = GetAbstracts(paper_list)

    # grab a bunch of physics papers
    paper_list = SearchPapers(sys.argv[2],n_negative)
    abstracts.extend(GetAbstracts(paper_list))

    #create vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    #permute abstracts in order of indices, then make a vector of 
    # word features
    abstracts = np.array(abstracts)[idxs]
    abstracts = list(abstracts)
    abstract_vectors = vectorizer.fit_transform(abstracts)

    #create target data and permute
    target_vector = np.concatenate((np.ones(n_positive),-1.*np.ones(n_negative)))
    target_vector = target_vector[idxs]
    
    #create perceptron classifier
    perceptron_classifier = PerceptronClassifier(abstract_vectors.shape[1],0.3)

    for k in range(abstract_vectors.shape[0]):
        x = []
        for j in range(abstract_vectors.shape[1]):
            x.append(abstract_vectors[(k,j)])

        x = np.array(x)
                     
        y_hat = perceptron_classifier.Predict(x)
        y = target_vector[k]
        print "-"*80
        if y_hat == 1:
            print "  "
            print "Perceptron indicates that this article is about {0}".format(sys.argv[1])
            print "  "
            if y == 1:
                print "This prediction is correct."
                print "  "
            else:
                print "This prediction is NOT correct."
                print "  "                
        else:
            print "  "
            print "Perceptron indicates that this article is about {0}".format(sys.argv[2])
            print "  "
            if y == -1:
                print "This prediction is correct."
                print "  "
            else:
                print "This prediction is NOT correct."
                print "  "                
            
        print abstracts[k]
        print "-"*80
        perceptron_classifier.Update(x,y_hat,y)
    
    print "Accuracy of Perceptron is ", perceptron_classifier.ReportAccuracy()


    #create perceptron classifier
    kernel_classifier = KernelPerceptronClassifier(abstract_vectors.shape[1],0.3,DotKernel)

    for k in range(abstract_vectors.shape[0]):
        x = []
        for j in range(abstract_vectors.shape[1]):
            x.append(abstract_vectors[(k,j)])

        x = np.array(x)
                     
        y_hat = kernel_classifier.Predict(x)
        y = target_vector[k]
        print "-"*80
        if y_hat == 1:
            print "  "
            print "Kernel Perceptron indicates that this article is about {0}".format(sys.argv[1])
            print "  "
            if y == 1:
                print "This prediction is correct."
                print "  "
            else:
                print "This prediction is NOT correct."
                print "  "                
        else:
            print "  "
            print "Kernel Perceptron indicates that this article is about {0}".format(sys.argv[2])
            print "  "
            if y == -1:
                print "This prediction is correct."
                print "  "
            else:
                print "This prediction is NOT correct."
                print "  "                
            
        print abstracts[k]
        print "-"*80
        kernel_classifier.Update(x,y_hat,y)
    
    print "Accuracy of Kernel Perceptron is ", kernel_classifier.ReportAccuracy()


        
    

    
    
    

    
    

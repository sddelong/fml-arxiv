import numpy as np
from ArxivData import TextFeatureVector
from ArxivData import FeaturizeAbstracts # for testing.

def sign(x):
    """ compute sign of x, with convention that 0 is positive """
    if x >= 0:
        return 1
    else:
        return -1

class OnlineSVMClassifier:
    """ Online SVM classifier for binary classification."""

    def __init__(self,C,eta):
        """ Constructor, takes parameter C used in the SVM algorithm. 

        Arguments:
                C - penalty parameter for SVM algorithm
                eta - learning rate
                
        """

        self.weights = dict()
        self.eta = eta
        self.C = C

        
    def Update(self,x,y_hat,y):
        """ given that the SVM has guessed y_hat for data x, update it 
        using the correct value y.

        Note: must be used after prediction to obtain a correct accuracy estimate, 
        Note: We may only update on some of the predictions where y_hat = -1 (undesireable paper).
        
        Note: y_hat is not directly used in this function, but is included for consistency with PerceptronClassifier Update function.
        """

        if(y*x.Dot(self.weights) < 1):
            x.UpdateWeightsSVM(self.weights,y,self.eta,self.C)
        else:
            x.UpdateWeightsSVM(self.weights,y,self.eta,0.0)
            
        return


    def Predict(self,x):
        """ predict y by using sign of w dot x """

        return sign(x.Dot(self.weights))
    
    def __repr__(self):
        
        repstring = 'Online SVM Classifier, eta = %1.3f, C = %1.3f'.format(self.eta, self.C)
        
        return repstring
    
    __str__ = __repr__
        


#wrapper functions to set up classifiers for testing
def MakeOnlineSVMClassifier(parameters):
    """ parameters are just eta """
    
    classifier = OnlineSVMClassifier(parameters[0],parameters[1])
    
    return classifier


if __name__ == "__main__":
    
    x = ["This is a Test Abstract"]
    x = FeaturizeAbstracts(x)[0]
    
    svmclassifier = OnlineSVMClassifier(0.3,0.2)
    
    y_hat = svmclassifier.Predict(x)
    
    assert y_hat == 1, "SVM should predict y_hat = 1 at initialization.  It does not."
    
    #update
    svmclassifier.Update(x,y_hat,-1)
    
    y_hat2 = svmclassifier.Predict(x)
    
    assert y_hat2 == -1, "SVM should predict y_hat = -1 after update"

    print "Completed some basic tests."

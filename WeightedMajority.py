""" Implement a simple weighted majority algorithm to combine multiple online learning algorithms and hopefully get a performance boost.



"""

from Perceptron import PerceptronClassifier
from Perceptron import VotedPerceptronClassifier
from Perceptron import KernelPerceptronClassifier
from Perceptron import MarginPerceptronClassifier
from Perceptron import MakeGaussianKernelPerceptronClassifier
from Perceptron import MakePolynomialKernelPerceptronClassifier
from OnlineSVM import OnlineSVMClassifier


def sign(x):
    """ compute sign of x, with convention that 0 is positive """
    if x >= 0:
        return 1
    else:
        return -1


class WeightedMajorityClassifier:
    
    def __init__(self, classifier_list):
        
        self.name = "Weighted Majority Classifier"
        self.classifier_list = classifier_list
        self.weights = [1. for k in classifier_list]
        
        self.beta = 1.0 #beta = 1, just majority vote seems to do best.
        
    def Predict(self,x):
        """ Predict by doing a weighted vote """
        
        value = 0.
        for k in range(len(self.classifier_list)):
            value += self.weights[k]*self.classifier_list[k].Predict(x)
        
        return sign(value)

    def Update(self,x,y_hat,y):
        """ given that the weighted majority has guessed y_hat for data x, 
        update it using the correct value y.

        Note: This assumes y != y_hat

        Note: must be used after prediction to obtain a correct accuracy estimate, 
        Note: We may only update on some of the predictions where y_hat = -1 (undesireable paper).
        """

        #update weights for weighted majority
        #update each classifier in classifier list if it's incorrect.
        for k in range(len(self.classifier_list)):
            if self.classifier_list[k].Predict(x) != y:
                self.weights[k] = self.beta*self.weights[k]
                self.classifier_list[k].Update(x,y_hat,y)
            else:
                #this subclassifier is correct:
                self.weights[k] = self.weights[k]/self.beta
            
        return


    
    def __repr__(self):
        
        repstring = "Weighted Majority Classifier using list of classifiers: " 
        for cl in self.classifier_list:
            repstring += str(cl)
        return repstring

    __str_ = __repr__
        
def MakeWeightedMajorityClassifier(parameters):
    """ wrapper to make weighted majority classifier from 
    Perceptron, Margin perceptron, SVM, Gaussian kernel Perceptron Classifier, Polynomial Kernel Perceptron Classifier
    
        inputs:
        parameters[0] - rho, margin for marginPerceptronClassifier
        parameters[1] - C, penalty for OnlineSVMClassifier 
    """

    pclassifier = PerceptronClassifier(1.0)
    v_pclassifier = VotedPerceptronClassifier(1.0)
    margin_pclassifier = MarginPerceptronClassifier(1.0, parameters[0])
    svmclassifier = OnlineSVMClassifier(parameters[1], 1.0)
    gk_pclassifier = MakeGaussianKernelPerceptronClassifier([1.0])
    pk_pclassifier = MakePolynomialKernelPerceptronClassifier([0.0, 3])
    

    classifier_list = [pclassifier, v_pclassifier, margin_pclassifier, svmclassifier, gk_pclassifier, pk_pclassifier]
    
    wm_classifier = WeightedMajorityClassifier(classifier_list)
    
    return wm_classifier
    
    

import numpy as np
from ArxivData import TextFeatureVector
from ArxivData import FeaturizeAbstracts #for testing.

def sign(x):
    """ compute sign of x, with convention that 0 is positive """
    if x >= 0:
        return 1
    else:
        return -1



class PerceptronClassifier:
    """ Simple perceptron algorithm for online learning. """
    
    def __init__(self,eta):
        """ Constructor for Perceptron. 

           Arguments:
                   eta - learning rate
        """
        self.eta = eta
        self.weights = dict()
        self.n_correct = 0
        self.n_wrong = 0
        
    def Update(self,x,y_hat,y):
        """ given that the Perceptron has guessed y_hat for data x, update it 
        using the correct value y.

        Note: must be used after prediction to obtain a correct accuracy estimate, 
        We will only update on some of the predictions where y_hat = -1 (undesireable paper).
        """
        if y_hat != y:
            #update
            self.n_wrong += 1
            x.UpdateWeights(self.weights,y,self.eta)
        else:
            self.n_correct += 1
        
        return
        
    def Predict(self,x):
        """ predict y by using sign of a dot product of x with weights """
        
        return sign(x.Dot(self.weights))

    def ReportAccuracy(self):
        
        return float(self.n_correct)/float(self.n_wrong + self.n_correct)


class KernelPerceptronClassifier():

    """ Simple perceptron algorithm for online learning, dual implementation 
    that can take a Kernel. This algorithm has to carry "Support Vectors" around with it.  
    """
    def __init__(self,eta,kernel):
        """ Constructor for Perceptron. 

           Arguments:
                   eta    - learning rate
                   kernel - kernel function to use, must be a PSD kernel that takes
                            two TextFeatureVectors and returns a scalar.
        """
        
        self.eta = eta
        self.alpha = []
        self.support_vecs = []
        self.support_labels = []
        self.kernel = kernel
        self.n_correct = 0
        self.n_wrong = 0
        
        
    def Update(self,x,y_hat,y):
        """ given that the Perceptron has guessed y_hat for data x, update it 
        using the correct value y.

        Note: must be used after every prediction to obtain a correct accuracy estimate
        """
        
        if y_hat != y:
            #update
            self.n_wrong += 1
            self.alpha.append(self.eta)
            self.support_vecs.append(x)
            self.support_labels.append(y)
        else:
            self.n_correct += 1
        
        return
        

    def Predict(self,x):
        """ predict y by using sign of a dot product of x with weights """
        
        f = 0
        for k in range(len(self.alpha)):
            f = f + self.alpha[k]*self.support_labels[k]*self.kernel(self.support_vecs[k],x)

        return sign(f)

    def ReportAccuracy(self):
        
        return float(self.n_correct)/float(self.n_wrong + self.n_correct)

""" Define some default kernels here to use with KernelPerceptronClassifier 
    Kernels operate on TextFeatureVectors. """

def DotKernel(x,y):
    """ simple dot kernel, gives the simple dual perceptron algorithm if used, 
        """

    #multiplication of TextFeatureVectors gives a dot product.
    return x*y

class WinnowClassifier():
    
    """ Simple Winnow algorithm for online learning. 
    
    TODO: this is not applicable with only positive features, need to think about this and perhaps
    modify to make something that will work with our problem. 
    """
    
    def __init__(self,n,eta):
        """ Constructor for Winnow. 

           Arguments:
                   eta - learning rate
                   n - length of input data. (We may want to do this differently
                            to be specific to bags of words)
        """
        
        self.eta = eta
        self.weights = np.ones(n)/n
        self.n_correct = 0
        self.n_wrong = 0
        
        
    def Update(self,x,y_hat,y):
        """ given that the algorithm has guessed y_hat for data x, update it 
        using the correct value y.

        Note: must be used after every prediction to obtain a correct accuracy estimate
        """
        
        if y_hat != y:
            #update
            self.n_wrong += 1

            Z_t = sum(self.weights*np.exp(self.eta*y*x))
            self.weights = self.weights*np.exp(self.eta*y*x)/Z_t
        else:
            self.n_correct += 1
        
        return

    def Predict(self,x):
        """ predict y by using sign of a dot product of x with weights """

        return sign(np.dot(self.weights,x))


    def ReportAccuracy(self):
        
        return float(self.n_correct)/float(self.n_wrong + self.n_correct)



if __name__ == "__main__":
    

    x = ["This is a test abstract"]
    x = FeaturizeAbstracts(x)
    pclassifier = PerceptronClassifier(0.3)
    
    y_hat = pclassifier.Predict(x[0])
    
    assert y_hat == 1, "y_hat for perceptron should be 1 at initialization, it is not"
    
    pclassifier.Update(x[0],y_hat,-1)
    y_hat_2 = pclassifier.Predict(x[0])
    
    assert y_hat_2 == -1, "y_hat should be -1 after update, it is not"

    
    #NOTE: Winnow currently unused
    wclassifier = WinnowClassifier(8,0.3)
    
    x = np.array([1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0])
    y_hat = wclassifier.Predict(x)

    assert y_hat == 1, "y_hat for winnow should be 1 at initialization for this x, it is not"
    
    wclassifier.Update(x,y_hat,-1)
    y_hat_2 = wclassifier.Predict(x)
    
    assert y_hat_2 == -1, "y_hat for winnow should be -1 after update, it is not"
    
    
    print "Completed some basic tests"




        

        
           
        

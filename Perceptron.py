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
        self.name = "Perceptron Classifier"
        
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

    def __repr__(self):
        
        repstring = 'Perceptron Classifier, eta = %1.3f' % self.eta
        
        return repstring
    
    __str__ = __repr__

    def ReportHighestWeights(self):
        #HACK: report the words with the largest absolute weights
        
        words_and_weights = [(self.weights[word],word) for word in self.weights]
            
        sort_wandw = sorted(words_and_weights, reverse=True)
        print "10 Most Positive words:"
        for k in range(10):
            print sort_wandw[k][1], sort_wandw[k][0]
        print "10 Most Negative words:"
        for k in range(10):
            print sort_wandw[-k][1], sort_wandw[-k][0]
            
            


#wrapper functions to set up classifiers for testing
def MakePerceptronClassifier(parameters):
    """ parameters are just eta """
    
    classifier = PerceptronClassifier(parameters[0])
    
    return classifier


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
        self.name = "Kernel Perceptron Clasifier"
        
        
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


def MakeGaussianKernel(sigma):
    """ create a function which is a 
    Gaussian Kernel exp(-||x - x'||^2/(2 sigma^2))
    """
    
    def GaussianKernel(x,y):
        
        return np.exp(x.Distance2(y)/(2.*sigma))
    
    return GaussianKernel
                      

def MakeGaussianKernelPerceptronClassifier(parameters):
    """ wrapper to make Gaussian Kernel Perceptron from a list of 
    parameters:
        parameters[0] = learning rate
        parameters[1] = sigma, variance of kernel
    """

    g_kernel = MakeGaussianKernel(parameters[1])
    
    kclassifier = KernelPerceptronClassifier(parameters[0],g_kernel)

    return kclassifier


def MakePolynomialKernel(c,d):
    """ create a function which is a 
    Polynomial Kernel 
    """
    
    def PolynomialKernel(x,y):
        
        return (x*y + c)**d
    
    return PolynomialKernel
                      

def MakePolynomialKernelPerceptronClassifier(parameters):
    """ wrapper to make Polynomial Kernel Perceptron from a list of 
    parameters:
        parameters[0] = c, constant offset
        parameters[1] = d, degree of polynomial kernel
        
        learning rate, eta, is set to a constant 1.0
    """

    p_kernel = MakePolynomialKernel(parameters[0],parameters[1])
    
    kclassifier = KernelPerceptronClassifier(1.0,p_kernel)

    return kclassifier


class MarginPerceptronClassifier():
    "Margin perceptron for online learning """
    
    def __init__(self,eta,rho):
        """ Constructor for margin perceptron, sets learning rate eta and
        margin rho """
        
        self.eta = eta
        self.rho = rho
        self.weights = dict()
        self.name = "Margin Perceptron Classifer"

    def Update(self,x,y_hat,y):
        """ Update classifier based on incorrect decision """
        
        #if weights  == 0
        
        w_norm = self.GetWNorm()
        
        if (w_norm == 0) or (y*x.Dot(self.weights)/w_norm < self.rho/2.):
            x.UpdateWeights(self.weights,y,self.eta)
            
        return

    def GetWNorm(self):
        """ Calculate 2-norm of the weight vector """
        value = 0.
        for word in self.weights:
            value += self.weights[word]**2
            
        value = np.sqrt(value)

        return value

    def Predict(self,x):
        """ predict y by using the sign of a dot product of x with weights """

        return sign(x.Dot(self.weights))        


    def __repr__(self):
        
        repstring = 'Margin Perceptron Classifier, eta = %1.3f, rho = %1.3f' % (self.eta, self.rho)
        
        return repstring


    __str__ = __repr__

def MakeMarginPerceptronClassifier(parameters):
    """ parameters are learning rate and margin, rho """

    margin_pclassifier = MarginPerceptronClassifier(parameters[0],parameters[1])

    return margin_pclassifier

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
        self.name = "Winnow Classifer"
        
        
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



    margin_pclassifier = MarginPerceptronClassifier(0.3,0.02)
    
    y_hat = margin_pclassifier.Predict(x[0])
    
    assert y_hat == 1, "y_hat for margin perceptron should be 1 at initialization, it is not"
    
    margin_pclassifier.Update(x[0],y_hat,-1)
    y_hat_2 = margin_pclassifier.Predict(x[0])
    
    assert y_hat_2 == -1, "margin perceptron y_hat should be -1 after update, it is not"

    #NOTE: Winnow currently unused
    wclassifier = WinnowClassifier(8,0.3)
    
    x = np.array([1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0])
    y_hat = wclassifier.Predict(x)

    assert y_hat == 1, "y_hat for winnow should be 1 at initialization for this x, it is not"
    
    wclassifier.Update(x,y_hat,-1)
    y_hat_2 = wclassifier.Predict(x)
    
    assert y_hat_2 == -1, "y_hat for winnow should be -1 after update, it is not"
    
    
    print "Completed some basic tests"




        

        
           
        

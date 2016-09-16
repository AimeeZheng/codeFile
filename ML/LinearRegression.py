import numpy as np
from scipy import linalg

class LinearRegression():
    """
    Ordinary least squares Linear Regression.

    Parameters
    ----------
    normalize : boolean, optional, default False
        If True, the regressors X will be normalized before regression.

    errorThreshold : condition of vonvergence
    
    max : max loop times
    
    Attributes
    ----------
    coef_ : array, shape (n_features, ) or (n_targets, n_features)
        Estimated coefficients for the linear regression problem.
        If multiple targets are passed during the fit (y 2D), this
        is a 2D array of shape (n_targets, n_features), while if only
        one target is passed, this is a 1D array of length n_features.

    Notes
    -----

    """

    def __init__(self, normalize = False, epsilon = 1, max = 1000):
        self.normalize = normalize
        self.epsilon = epsilon
        self.max = max


    def train(self, X, y):
        """
        Train linear model.(the normal equation)

        Parameters
        ----------
        X : numpy array or sparse matrix of shape [n_samples, n_features]
            Training data

        y : numpy array of shape [n_samples, n_targets]
            Target values

        Returns
        -------
        self : returns an instance of self.
        """
        m, n = X.shape
        if y.shape[0] != m:
            raise ValueError('incompatible dimensions')
        X = np.c_[[1 for i in range(m)], X]
        X_transpose = X.T
        self.coef_ = linalg.inv(X_transpose.dot(X)).dot(X_transpose.dot(y))       
        return self
    
    def batch(self, X, y, alpha = 0.001):
        """
        Train linear model.(batch gradient descent)

        Parameters
        ----------
        X : numpy array or sparse matrix of shape [n_samples, n_features]
            Training data

        y : numpy array of shape [n_samples, n_targets]
            Target values
            
        alpha: learning rate

        Returns
        -------
        self : returns an instance of self.
        """
        m, n = X.shape
        if y.shape[0] != m:
            raise ValueError('incompatible dimensions')
        coef = np.array([np.float(0) for i in range(n + 1)])
        #x0 = 1
        X = np.c_[[1 for i in range(m)], X]
        h = X.dot(coef)
        cost_new = J_theta(y, h)
        k = 0
        while True:
            error = np.array([y[i] - h[i] for i in range(m)])
            coef += alpha * (error.dot(X))
            h = X.dot(coef)
            cost = cost_new
            cost_new = J_theta(y, h)
            #print(k, cost_new)
            k += 1
            if abs(cost_new - cost) < self.epsilon or (k > self.max):
                break
        self.coef_ = coef
        return self
        
    def stochastic(self, X, y, alpha = 0.001):
        """
        Train linear model.(stochastic gradient descent)

        Parameters
        ----------
        X : numpy array or sparse matrix of shape [n_samples, n_features]
            Training data

        y : numpy array of shape [n_samples, n_targets]
            Target values
            
        alpha: learning rate

        Returns
        -------
        self : returns an instance of self.
        """
        m, n = X.shape
        if y.shape[0] != m:
            raise ValueError('incompatible dimensions')
        coef = np.array([np.float(0) for i in range(n + 1)])
        X = np.c_[[1 for i in range(m)], X]
        h = X.dot(coef)
        cost_new = J_theta(y, h)
        k = 0
        while True:
            for i in range(m):
                error = y[i] - h[i]
                coef += alpha * error * X[i]
            h = X.dot(coef)
            cost = cost_new
            cost_new = J_theta(y, h)
            #print(k, cost_new)
            k += 1
            if abs(cost_new - cost) < self.epsilon or (k > self.max):
                break
        self.coef_ = coef
        return self
        
    def predict(self, X):
        """
        Predict using the linear model

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape = (n_samples,)
            Returns predicted values.
        """
        X = np.c_[[1 for i in range(X.shape[0])], X]
        return np.dot(X, self.coef_)

def J_theta(y, h):
    m = y.shape[0]
    cost = 0
    for i in range(m):
        cost += (y[i] - h[i]) ** 2
    return cost / 2






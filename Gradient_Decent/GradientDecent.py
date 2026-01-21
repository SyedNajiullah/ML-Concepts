import numpy as np

def gradient_decent(x, y):
    m_current = b_current = 0
    iterations = 10000 #epoch
    n = len(x) # number of rows
    learning_rate = 0.08 # learning rate (step size)
    
    for i in range(iterations):
        y_predicted = m_current * x + b_current # prediction
        cost = (1/n) * sum([val**2 for val in (y-y_predicted)]) # cost funcion (mean squared error)
        md = -(2/n)*sum(x*(y-y_predicted)) # partial derivative with respect to m
        bd = -(2/n)*sum((y-y_predicted)) # partial derivative with respect to b
        m_current = m_current - learning_rate * md # updating m
        b_current = b_current - learning_rate * bd # updating b
        print(f"m: {m_current}, b: {b_current}, cost: {cost}, iterations: {i}")
        
x = np.array([1, 2, 3, 4, 5]) # input 
y = np.array([5, 7, 9, 11, 13]) # real output

gradient_decent(x, y)
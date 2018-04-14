# -*- coding: utf-8 -*-
import math
import random

def rand(a, b):
    return (b - a) * random.random() + a

def make_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def purelin(x): 
    return x

def purelin_derivative(x):
    return 1

def sigmoid_derivative(x):
    return x * (1 - x)

class RNN:
    def __init__(self):
        self.input_n              = 0
        self.hidden_n             = 0
        self.output_n             = 0
        self.T                    = 0
        self.input                = []
        self.hidden               = []
        self.prehidden            = []
        self.output               = []
        self.input_weights        = []
        self.output_weights       = []
        self.hidden_weigths       = []
        self.hidden_future_deltas = []
        self.alpha                = 0
        self.gama                 = 0
      

    def setup(self, ni, nh, no, T, gama, alpha):
        self.input_n  = ni
        self.hidden_n = nh
        self.output_n = no
        self.T        = T
        self.alpha    = alpha
        self.gama     = gama
       
        self.input_weights  = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        self.hidden_weights = make_matrix(self.hidden_n, self.hidden_n)

        for x in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[x][h]    = rand(-0.2, 0.2)           
        for h in range(self.hidden_n):
            for y in range(self.output_n):
                self.output_weights[h][y]   = rand(-0.2, 0.2)
        for h1 in range(self.hidden_n):
            for h2 in range(self.hidden_n):
                self.hidden_weights[h1][h2] = rand(-0.2, 0.2)


    def predict(self, inputdata):
        inputs    = inputdata
        hidden    = [0] * self.hidden_n
        output    = [0] * self.output_n

        # 前向 隐含层输出
        for h in range(self.hidden_n):
            total_1 = 0.0
            for x in range(self.input_n):
                total_1 =  total_1 + inputs[x] * self.input_weights[x][h]
            hidden[h] = sigmoid(total_1)

        #前向 输出层输出
        for y in range(self.output_n):
            total = 0.0
            for h in range(self.hidden_n):
                total = total + hidden[h] * self.output_weights[h][y]
        
            output[y] = purelin(total)
        
        return output

    def predict_back(self, inputss, labels):
        Error = 0

        inputs    = inputss
        hidden    = make_matrix(self.T, self.hidden_n)
        prehidden = make_matrix(self.T, self.hidden_n)
        output    = make_matrix(self.T, self.output_n)

        x_whh_delats      = make_matrix(self.hidden_n, self.hidden_n)
        x_whh_past_delats = make_matrix(self.hidden_n, self.hidden_n)
        
        for t in range(self.T):

            u            = [0] * self.hidden_n#u_t
            v            = [0] * self.output_n#v_t
            w            = [0] * self.hidden_n

            # 前向 隐含层输出
            for h in range(self.hidden_n):
                total_1 = 0.0
                if(t>0):
                    for x in range(self.input_n):
                        total_1 =  total_1 + inputs[t-1][x] * self.input_weights[x][h]
                total_2 = 0.0
                for h2 in range(self.hidden_n):
                    total_2 = total_2 + prehidden[t][h2] * self.hidden_weights[h2][h]
                
                u[h] = total_1 + total_2
                hidden[t][h] = sigmoid(total_1 + total_2)

            #承接层
            if(t>0):
                for h in range(self.hidden_n):
                    prehidden[t][h] = self.alpha *prehidden[t-1][h] + hidden[t-1][h] 
            
            #前向 输出层输出
            for y in range(self.output_n):
                total = 0.0
                for h in range(self.hidden_n):
                    total = total + hidden[t][h] * self.output_weights[h][y]
                v[y] = total
                output[t][y] = purelin(total)
            
            #输出层误差， delta_y_t
            output_deltas = [0.0] * self.output_n
            for y in range(self.output_n):
                error = 0
                error = labels[t][y] - output[t][y]
                Error = Error + error 
                output_deltas[y] = purelin_derivative(v[y]) * error

            #隐含层误差， delta_h_t
            hidden_deltas = [0.0] * self.hidden_n
            
            for h1 in range(self.hidden_n):
                error_2 = 0.0
                for y in range(self.output_n):
                    error_2 = error_2 + output_deltas[y] * self.output_weights[h1][y]
                w[h1] = error_2   
                hidden_deltas[h1] = sigmoid_derivative(u[h1]) * (error_2)
              
            #W_hy增量
            for h in range(self.hidden_n):
                for y in range(self.output_n):
                    self.output_weights[h][y]   = self.output_weights[h][y]+ self.gama * output_deltas[y]*hidden[t][h]
                    
            #W_xh增量
            if(t>0):
                for x in range(self.input_n):
                    for h in range(self.hidden_n):
                        self.input_weights[x][h]    =self.input_weights[x][h]+ self.gama * hidden_deltas[h]*inputs[t-1][x]
                   
            #W_hh增量
            if(t>0):
                for j in range(self.hidden_n):
                    for l in range(self.hidden_n):
                        x_whh_delats[j][l] = self.alpha * x_whh_past_delats[j][l] +\
                                 prehidden[t-1][j] * sigmoid_derivative(u[j])
            x_whh_past_delats = x_whh_delats

            for j in range(self.hidden_n):
                for l in range(self.output_n):
                    self.hidden_weights[j][l] = self.hidden_weights[j][l]+ self.gama * x_whh_delats[j][l] * w[j]
        
        return Error

    def train(self, cases, labels, limit=1000, wucha=1.0e-02):
        for j in range(limit):
            
            error = self.predict_back(cases, labels)
            #print('limit', j,error)
            if(abs(error)<wucha):
                break
            
       
#trainX=[[0.4413,0.4707,0.6953,0.8133,0.4379,0.4677,0.6981,0.8002,0.4517,0.4725,0.7006,0.8201],\
        #[0.4379,0.4677 ,0.6981, 0.8002 ,0.4517 ,0.4725, 0.7006, 0.8201 ,0.4557, 0.4790, 0.7019 ,0.8211],\
        #[0.4517, 0.4725, 0.7006 ,0.8201, 0.4557 ,0.4790 ,0.7019 ,0.8211 ,0.4601 ,0.4811, 0.7101, 0.8298]]
#trainY=[[0.4557 ,0.4790 ,0.719 ,0.8211],[0.4601 ,0.4811 ,0.7101 ,0.8298], [0.4612 ,0.4845 ,0.7188 ,0.8312]]

    
    
    

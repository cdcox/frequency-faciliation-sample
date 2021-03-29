# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 10:29:34 2021

@author: coxbox
"""
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def load_real_data(file_name):
    '''Loading in real data and finding frequencies as defined by headers in CSV'''
    freq_targets = np.genfromtxt(file_name,delimiter=',',skip_header=1,dtype ='float')
    col_names = np.genfromtxt(file_name,delimiter=',',dtype ='int')[0,:].tolist()
    real_data_for_error_calc = dict()
    for cnn,col_name in enumerate(col_names):
        real_data_for_error_calc[col_name] = freq_targets[:,cnn]
    return real_data_for_error_calc
    

def initialize(param_dict,result):
    ''' Takes in parameters and generates intial state values and stores it'''  
    glu = 0
    Cai = 0
    Prel = param_dict['Prel0']
    Rrel = 1
    krecov = param_dict['krecov0']
    ICa=0
    result['glu'][freqs]=[glu]
    result['Cai'][freqs]=[Cai]
    result['Prel'][freqs]=[Prel]
    result['Rrel'][freqs]=[Rrel]
    result['ICa'][freqs]=[ICa]
    state_values = [glu, Cai, Prel, Rrel,krecov,ICa]
    return state_values,result

def observe(state_values,result):
    ''' Stores state values outside glu these values are "extra" and are mostly
    collected to  allow for debugging/further investigation. When running larger
    scale muitple sample runs, it often makes sense to not collect anything but
    glu'''
    glu, Cai, Prel, Rrel,krecov,ICa = state_values
    result['glu'][freqs].append(glu)
    result['Cai'][freqs].append(Cai)
    result['Prel'][freqs].append(Prel)
    result['Rrel'][freqs].append(Rrel)
    result['ICa'][freqs].append(ICa)
    return result
    

def update(state_values,param_dict,t_spike,measure_pts):
    ''' Takes in parameters and state and updates state based on dynamics Eqs
    from Lee, Antom,Poon Mcrae 2009'''
    
    #Load parameters and state
    KCa = param_dict['KCa']
    tauCai = param_dict['tauCai']
    krecov0 = param_dict['krecov0']
    krecovmax = param_dict['krecovmax']
    Prel_max = param_dict['Prel_max']
    n = 4
    nTot = 1
    glu,Cai,Prel,Rrel,krecov,ICa = state_values
    
    #Run one time step
    input_sum = 0
    dirac_time_test = (t_spike>=tminus1) * (t_spike<t)
    if np.sum(dirac_time_test)>0:
        input_sum=1
        measure_pts.append(t)
    ICa = KCa*input_sum
    dCai_dt = ((-Cai + Cai0))/tauCai+ICa #Paper has ICa/TauCai I unwound this for clarity
    new_krecov = krecov0+(krecovmax-krecov0)*Cai/(Cai+krecov)
    dRrel_dt = krecov*(1-Rrel)- (Prel*Rrel*input_sum) #Slightly modified from paper
    new_Prel = Prel_max*(Cai**4)/(Cai**4+Krel**4)
    dglu_dt = n*nTot*Rrel*Prel*input_sum
    glu = dglu_dt
    Cai = Cai+dCai_dt
    Prel = new_Prel
    Rrel = dRrel_dt+Rrel
    krecov = new_krecov
    state_values = [glu, Cai, Prel, Rrel,krecov,ICa]
    return state_values,measure_pts

def SSE_and_val_extract(real,calculated,measurepts):
    '''extract points from  real data set for comparison and calcualted sum square error'''
    calc_measure = calculated[measurepts]
    SSE = np.sum(np.square(np.subtract(real,calc_measure)))
    return SSE,calc_measure
       
if __name__ =='__main__':
    data_csv = 'CA1.csv'
    real_data_for_error_calc = load_real_data(data_csv)
    
    #adding and packing parameters, current values based on state space search
    Cai0 = 32#uM Calcium increase per influc
    KCa = 64#uMms-1 Rate of calcium efflux
    krecov0 =7.5*10**-3#ms-1 Intial rate of RRP reset
    krecovmax = 2.8*10**-2#ms-1 Max rate of RRP reset
    Krel = 32 #uM Calcium sensitivery of transmitter release
    Prel_max = 1# probability Max release per spike
    Prel0 = 0.29# probability Intial release per spike
    tauCai =25 # Rate of calcium exit
    n=4
    param_dict = {'Cai0':Cai0, 'KCa':KCa,'krecov0':krecov0,
                  'krecovmax':krecovmax,'Krel':Krel,'Prel_max':Prel_max,
                  'Prel0':Prel0,'tauCai':tauCai}
    result = {'glu':{},'Cai':{},'Prel':{},'Rrel':{},'ICa':{}}
    
    for freqs in real_data_for_error_calc.keys():
        freq = freqs
        total_spikes =10
        step2 = 1000/freq
        t_spike = np.arange(0,total_spikes*step2,step2) #spiking time based on frequency
        step=1
        measure_pts = [] #captures time of spikes
        state_values,result = initialize(param_dict,result)
        for t in np.arange(1000):
            tminus1=t
            t=t+step
            state_values,measure_pts = update(state_values,param_dict,t_spike,measure_pts)
            result = observe(state_values,result)
            
        #Glu values are most comparable to the frequency facilitation values also normalize to 100
        values_to_compare = np.array(result['glu'][freqs])/result['glu'][freqs][1]*100
        real_data = real_data_for_error_calc[freqs]
        SSE,calc_measure = SSE_and_val_extract(real_data,values_to_compare,measure_pts)
        
        plt.figure()
        plt.xlabel('Pulse number')
        plt.ylabel('% first pulse')
        plt.plot(calc_measure)
        plt.plot(real_data)
        plt.legend(['Simulated Values','Real Values'])
        plt.title('Frequency: '+str(freqs)+' Hz'+' SSE is '+ str(np.round(SSE))+' vs '+data_csv[:-4])
        plt.savefig('FF '+str(freqs)+' Hz'+'.png')

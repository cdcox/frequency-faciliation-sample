# Frequency Facilitation Sample

## Goal

The goal of this is to creat a model of frequency facilitation to probe the properties of various regions of the hippocampus and cortex. A biophysical model is probably not required as the synpatic system can be approxximated as a balance between the number of synaptic sites available and the probability of release, with a refresh rate based on the recovery time of the ready releasable pool. As multiple inputs come in, the synaptic calcium increases leading to a higher probability of release as the synaptic pools are depleted. If depletion 'wins out' as in the case of a long recovery time or high intial probability of release (many synaptic sites depleted), then there will be depression. If, however calcium build up wins out low intiail release probability or sufficeintly rapid recovery of ready releasable pool, there will be facilitation.


## Model

This is a basic dynamical system equation model. It takes basic parameters of the readily releaseable pool and probability of release and generates graphs of the responsesat various frequencys. It also compares these values to existing data as a sum-square error. It is currently rate locked at 1000 samples per second. Adjustment of this should invovle altering the various parameters.

This code is based on the following equations from [A kinetic model unifying presynaptic short-term facilitation and depression Chuang-Chung J Lee 1, Mihai Anton, Chi-Sang Poon, Gregory J McRae 2009](https://pubmed.ncbi.nlm.nih.gov/19093195/)

A likely output input and output are included below for frequency facilitation in the CA1:

CA1 output at 10Hz of a model found through a large scale state-space search.

![png](FF%2010%20Hz.png) 



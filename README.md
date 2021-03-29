# Frequency Facilitation Sample

## Goal

The goal of this is to create a model of frequency facilitation to probe the properties of various regions of the hippocampus and cortex. A biophysical model is probably not required as the synaptic system can be approximated as a balance between the number of synaptic sites available and the probability of release, with a refresh rate based on the recovery time of the ready-releasable pool. As multiple inputs come in, the synaptic calcium increases leading to a higher probability of release as the synaptic pools are depleted. If depletion 'wins out' as in the case of a long recovery time or high initial probability of release (many synaptic sites depleted), then there will be depression. If, however calcium build up wins out low initial release probability or sufficiently rapid recovery of ready-releasable pool, there will be facilitation.


## Model

This is a basic dynamic system equation model. It takes basic parameters of the ready-releasable pool and probability of release and generates graphs of the responses at various frequencies. It also compares these values to existing data as a sum-square error. It is currently rate locked at 1000 samples per second. Adjustment of this will involve altering the various parameters.

This code is based on equations from [A kinetic model unifying presynaptic short-term facilitation and depression. Chuang-Chung J Lee, Mihai Anton, Chi-Sang Poon, Gregory J McRae 2009](https://pubmed.ncbi.nlm.nih.gov/19093195/)

A likely input and output are included below for frequency facilitation in the CA1:

CA1 output at 10Hz of a model found through a large scale state-space search.

![png](FF%2010%20Hz.png) 

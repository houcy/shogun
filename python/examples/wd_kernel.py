from numpy import *
from numpy.random import *
from shogun.Features import *
from shogun.SVM import *
from shogun.Kernel import *

num_dat=50
len=70
acgt=array(['A','C','G','T'])

#generate train data
trdat=chararray((len,2*num_dat),1,order='FORTRAN')
trlab=concatenate((-ones(num_dat,dtype=double), ones(num_dat,dtype=double)))
trdat[:]=acgt[array(floor(4*random_sample(2*num_dat)), dtype=int)]
trdat[10:15,trlab==1]='A'
trainfeat = CharFeatures(trdat,DNA)
trainlab = Labels(trlab)

#generate test data
tedat=chararray((len,2*num_dat),1,order='FORTRAN')
telab=concatenate((-ones(num_dat,dtype=double), ones(num_dat,dtype=double)))
tedat[:]=acgt[array(floor(4*random_sample(2*num_dat)), dtype=int)]
tedat[10:15,telab==1]='A'
testfeat = CharFeatures(tedat,DNA)
testlab = Labels(telab)

#train svm
weights=ones(20,dtype=double)
wdk=WeightedDegreeCharKernel(trainfeat,trainfeat, 10, weights)
svm = SVMLight(10, wdk, trainlab)
svm.set_linadd_enabled(True)
#svm.set_linadd_enabled(False)
svm.set_batch_computation_enabled(True)
#svm.set_batch_computation_enabled(False)
svm.train()
print svm.get_num_support_vectors()
trainout=svm.classify().get_labels()

#test
wdk_test=WeightedDegreeCharKernel(trainfeat,testfeat, 10, weights)
svm.set_kernel(wdk_test)
#svm.init_kernel_optimization()
testout=svm.classify().get_labels()

k=wdk.get_kernel_matrix()
print trainout
print testout

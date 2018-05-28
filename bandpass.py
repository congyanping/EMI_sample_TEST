import numpy as np
import h5py
import matplotlib.pyplot as plt

fig,ax = plt.subplots(4,2,figsize = (9,16))


    
fil = h5py.File("/home/congyanping/Desktop/EMI_sample_test/bandpass_crosstalk_test/output_rfi_with_New_Multi_Win_11-17_index_1/nc/0/file_0.hdf5",'r')
i = -2
data = fil["vis"][...][:,:,i]
bl_label = fil["blorder"][...]
#print 'bl_label',bl_label[i]
#print 'oo',bl_label[np.where(bl_label[:,0] == bl_label[:,1])]
ns_on = fil["ns_on"][...]
data[ns_on,:] = 0.0
       


def Plot(ndarray,name = ''):
    #plt.figure(1)
    ax[0,0].imshow(np.abs(ndarray),aspect='auto')
    ax[0,0].set_ylabel("integration time")
    ax[0,0].set_xlabel("frequency")
    #plt.savefig(name)
    #plt.show()
def Plot_2(ndarray=None,name = '',ns_on=ns_on):
    #plt.figure(2)
    i=9
    ndarray = fil["vis"][...][:,:,i]
    print 'ns_on',ns_on
    ndarray = np.mean(ndarray,axis=1)
    ndarray = np.abs(ndarray)
    ndarray[ns_on] = np.nan
    ax[0,1].plot(range(ndarray.shape[0]),ndarray,label = "baseline" + str(bl_label[i]))
    ax[0,1].legend(loc=0)
    ax[0,1].set_ylabel("abs(v_ij)")
    ax[0,1].set_xlabel("integration time")
    #plt.show()
def Plot_3(ndarray):
    #plt.figure(1)
    #ndarray = np.abs(ndarray)
    casA = ndarray[750:875,:]
    #before = ndarray[700:750,:]
    #after = ndarray[875:925,:]
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    casA = np.abs(casA)
    casA = np.mean(casA,axis=0)
     
    before = np.mean(before,axis=0)
    after = np.mean(after,axis=0)
    before = np.abs(before)
    after = np.abs(after)
    
    casA = np.log10(casA)
    before = np.log10(before)
    after = np.log10(after)
    
    result = casA - 0.5*(before+after)
    
    for ind,value in enumerate([casA,before,after]): #,result]):
        index = ["casA","before","after"] #,"bandpass"]
        ax[1,0].plot(range(value.shape[0]),value,label=index[ind])
        ax[1,0].legend(loc=0,ncol=1)
        ax[1,0].set_ylabel("amplitude")
    ax[2,0].plot(range(result.shape[0]),result,label="T_sky*G_a*G_e")
    ax[2,0].legend(loc=0,ncol=1)
    ax[2,0].set_ylabel("amplitude")
    ax[2,0].set_xlabel("frequency")
    #plt.show()
#use noise source data and no-substract system noise
def Plot_4(ndarray=True,name=''):
    num = list(np.where(bl_label[:,0] == bl_label[:,1])[0])
    auto1 = fil["vis"][...][:,:,num[0]].copy()
    
    auto2 = fil["vis"][...][:,:,num[6]].copy()
    #print '4auto1',np.abs(auto1)
    auto1 = auto1[ns_on,:] 
    auto2 = auto2[ns_on,:] 
    
    auto1 = np.nanmean(auto1,axis=0)
    auto2 = np.nanmean(auto2,axis=0)
    
    #print  '4meanauto1',np.abs(auto1)
    sqrt_auto = np.sqrt(auto1*auto2)
    
    feed1 = bl_label[num[0]][0]
    feed2 = bl_label[num[6]][0]
    
    #plot auto1 and auto2 
    print 'feed',feed1,feed2
    for j,i in enumerate([auto1,auto2]):
        label = ["auto1","auto2"]
        ax[1,1].plot(range(i.shape[0]),np.abs(i),label = label[j] )
        ax[1,1].legend(loc=1)
        
    for ind,value in enumerate(bl_label):       
        if value[0]==feed2 and value[1]==feed1:
            print 'index',ind
            print bl_label[ind]
            cross = fil["vis"][...][:,:,ind]
    cross = cross[ns_on,:] 
    cross = np.nanmean(cross,axis=0)
    
    #ratio = np.abs(sqrt_auto)/np.abs(cross) 
    #differ = sqrt_auto - cross
    #print 'ratio',ratio
   
    sqrt_auto = np.abs(sqrt_auto) #- np.abs(np.mean(differ))
    cross = np.abs(cross)
    print 'sqrt',sqrt_auto
    print 'cross',cross
    
    for j,i in enumerate([sqrt_auto,cross]):
        label = ["sqrt(auto1*auto2)","cross"]
        ax[2,1].plot(range(i.shape[0]),i,label = label[j] )
        ax[2,1].legend(loc=1)
        ax[2,1].grid(True)
    return 
#use noise source data and do substract system noise    
def Plot_5():
    num = list(np.where(bl_label[:,0] == bl_label[:,1])[0])
    print 'equal_label',num,bl_label[num]
    
    auto1 = fil["vis"][...][:,:,num[0]].copy()
    #auto1[ns_on,:] = np.nan
    ndarray = auto1
    
    casA = ndarray[750:875,:]   
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    #casA = np.abs(casA)
    casA = np.nanmean(casA,axis=0).reshape(-1)     
    before = np.nanmean(before,axis=0).reshape(-1)
    after = np.nanmean(after,axis=0).reshape(-1)
    
    #before = np.abs(before)
    #after = np.abs(after)
    
    #casA = np.log10(casA)
    #before = np.log10(before)
    #after = np.log10(after)
    print 'casA.shape',casA.shape,before.shape,after.shape
    auto1 = auto1[ns_on,:]     
    auto1 = np.nanmean(auto1,axis=0)
    
    bandpass1 = auto1 - 0.5*(before+after)
    #bandpass1 = 0.5 * (before + after)
    #bandpass1 = np.nanmean(ndarray,axis = 0)
    auto1 = bandpass1
    
    auto2 = fil["vis"][...][:,:,num[6]].copy()
    #auto2[ns_on,:] = np.nan
    ndarray = auto2
    
    casA = ndarray[750:875,:]   
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    #casA = np.abs(casA)
    casA = np.nanmean(casA,axis=0)
    before = np.nanmean(before,axis=0)
    after = np.nanmean(after,axis=0)
    
    #before = np.abs(before)
    #after = np.abs(after)
    
    #casA = np.log10(casA)
    #before = np.log10(before)
    #after = np.log10(after)
    auto2 = auto2[ns_on,:]     
    auto2 = np.nanmean(auto2,axis=0)
    bandpass2 = auto2 - 0.5*(before+after)
    #bandpass2 = 0.5*(before + after)
    #bandpass2 = np.nanmean(ndarray,axis=0)
    auto2 = bandpass2
    
    print 'bandpass1.shape',bandpass1.shape
    print 'bandpass2.shape',bandpass2.shape
       
    print 'index(auto1)<0',np.where(auto1<0)
    print 'index(auto2)<0',np.where(auto2<0)
    
    sqrt_auto = np.abs(np.sqrt(auto1*auto2))
    print 'sqrt_auto.shape',sqrt_auto.shape
    #cross
    feed1 = bl_label[num[0]][0]
    feed2 = bl_label[num[6]][0]
    
    for ind,value in enumerate(bl_label):        
        if value[0]==feed2 and value[1]==feed1:
            print 'index',ind
            print bl_label[ind]
            ccross = fil["vis"][...][:,:,ind]
    
   
    ccross = ccross[ns_on,:] 
    ccross = np.nanmean(ccross,axis=0)
    ccross = np.abs(ccross)
 
    print 'ccross.shape',ccross
    #ratio = np.mean(np.abs(cross) / np.abs(sqrt_auto))
    #sqrt_auto = np.abs(sqrt_auto) * ratio
    
    #print 'mean ratio',ratio
    #end cross
    #ax[1,1].plot(range(auto1.shape[0]),auto1,label = 'auto1')
    #ax[1,1].plot(range(auto2.shape[0]),auto2,label = 'auto2')
    #ax[1,1].legend(loc=1)
    
    #ax[2,1].plot(range(sqrt_auto.shape[0]),np.log10(sqrt_auto),label = "sqrt(auto1*auto2)_do_sub")
    #ax[2,1].set_ylabel('log=True')
    #ax[2,1].legend(loc=1)
    #ax[2,1].grid(True)
    for j,i in enumerate([sqrt_auto,ccross]):
        label = ["sqrt(auto1*auto2)_do_subtraction","cross"]
        ax[3,1].plot(range(i.shape[0]),i,label = label[j] )
        
    #ax[3,1].plot(range(cross.shape[0]),np.log10(cross),label = 'cross_with_log')
    ax[3,1].set_ylabel('log=True')
    ax[3,1].legend(loc=1)
    ax[3,1].grid(True)               
    return 
    
def Plot_6():
    num = list(np.where(bl_label[:,0] == bl_label[:,1])[0])
    
    auto1 = fil["vis"][...][:,:,num[0]].copy()
    auto1[ns_on,:] = np.nan
    ndarray = auto1
    
    casA = ndarray[750:875,:]   
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    
    casA = np.nanmean(casA,axis=0).reshape(-1)     
    before = np.nanmean(before,axis=0).reshape(-1)
    after = np.nanmean(after,axis=0).reshape(-1)
       
    bandpass1 = casA - 0.5*(before+after)
    #auto1 = np.nanmean(auto1,axis=0)
    auto1 = bandpass1
    
    auto2 = fil["vis"][...][:,:,num[6]].copy()
    auto2[ns_on,:] = np.nan
    ndarray = auto2
    
    casA = ndarray[750:875,:]   
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    
    casA = np.nanmean(casA,axis=0)
    before = np.nanmean(before,axis=0)
    after = np.nanmean(after,axis=0)
    
    bandpass2 = casA - 0.5*(before+after)

    #auto2 = np.nanmean(auto2,axis=0)
    auto2 = bandpass2
      
    sqrt_auto = np.abs(np.sqrt(auto1*auto2))
    
    feed1 = bl_label[num[0]][0]
    feed2 = bl_label[num[6]][0]
    
    for ind,value in enumerate(bl_label):        
        if value[0]==feed2 and value[1]==feed1:
            print 'index',ind
            print bl_label[ind]
            ccross = fil["vis"][...][:,:,ind]
    
    ccross[ns_on,:] = np.nan
    ndarray = ccross
    
    casA = ndarray[750:875,:]   
    before = ndarray[500:600,:]
    after = ndarray[1125:1250,:]

    
    casA = np.nanmean(casA,axis=0)
    before = np.nanmean(before,axis=0)
    after = np.nanmean(after,axis=0)
    
    ccross = casA - 0.5*(before+after)
    #ccross = np.nanmean(ccross,axis = 0)
    #ccross[ns_on,:] = np.nan 
    #ccross = np.nanmean(ccross[750:875,:],axis=0)
    ccross = np.abs(ccross)
    print 'final_cross',ccross[0:6]
    
    for j,i in enumerate([sqrt_auto,ccross]):
        label = ["sqrt(auto1*auto2)","cross"]
        ax[3,0].plot(range(i.shape[0]),i,label = label[j] )
        

    ax[3,0].set_ylabel('log=True')
    ax[3,0].legend(loc=1)
    ax[3,0].grid(True)               
    return 



Plot(data)
Plot_2()
#Plot_2(data)
Plot_3(data)
Plot_4()
Plot_5()
Plot_6()
plt.show()


import pdb
import sys

orgdata={}

class datanode:
    def __init__(self, _userid,_utradeidfirst,
    _utradeidsecond,_orgidfirst,_orgidsecond,_orgidthird,
    _firstconsumemonth,_pcconsume,_pcclick,_wlconsume,_wlclick):
        self.userid=_userid
        self.utradeidfirst=_utradeidfirst
        self.utradeidsecond=_utradeidsecond
        self.orgidfirst=_orgidfirst
        self.orgidsecond=_orgidsecond
        self.orgidthird=_orgidthird
        self.firstconsumemonth=_firstconsumemonth
        self.pcconsume=_pcconsume
        self.pcclick=_pcclick
        self.wlconsume=_wlconsume
        self.wlclick=_wlclick

def getpos(date):
    year_init=2008
    month_init=1
    year=int(date[0:4])
    month=int(date[5:7])
    pos=(year-year_init)*12+(month-month_init)
    return(pos)

def readline():
    n=0
    filename=open("loss_charge.txt")
    t_userid=None
    t_consumelist=[0 for n in range(0,100)]
    t_clicklist=[0 for n in range(0,100)]
    t_consumelist_wl=[0 for n in range(0,100)]
    t_clicklist_wl=[0 for n in range(0, 100)]
    t_utradeidfirst=None
    t_utradeidsecond=None
    t_orgidfirst=None
    t_orgidsecond=None
    t_orgidthird=None
    t_firstconsumemonth=None
    
    for line in filename.readlines():
        info=line.split('\t')
        if info[0]==t_userid:
            pos=getpos(info[1])
            #pdb.set_trace()
            if info[7]=='pc':
                t_consumelist[pos]=float(info[9])
                t_clicklist[pos]=int(info[10])
            else:
                t_consumelist_wl[pos]=float(info[9])
                t_clicklist_wl[pos]=int(info[10])
        else:
            if t_userid:
                #pdb.set_trace()
                detail_info=datanode(t_userid, t_utradeidfirst,
                t_utradeidsecond,t_orgidfirst,
                t_orgidsecond,t_orgidthird,t_firstconsumemonth,t_consumelist,t_clicklist,
                t_consumelist_wl, t_clicklist_wl)
                orgdata[t_userid]=detail_info
           
            t_userid=info[0]
            t_consumelist=[0 for n in range(0,100)]
            t_clicklist=[0 for n in range(0,100)]
            t_consumelist_wl=[0 for n in range(0,100)]
            t_clicklist_wl=[0 for n in range(0,100)]
            t_utradeidfirst=info[2]
            t_utradeidsecond=info[3]
            t_orgidfirst=info[4]
            t_orgidsecond=info[5]
            t_orgidthird=info[6]
            t_firstconsumemonth=info[8]
            pos=getpos(info[1])
            if info[7]=='pc':
                t_consumelist[pos]=float(info[9])
                t_clicklist[pos]=int(info[10])
            else:
                t_consumelist_wl[pos]=float(info[9])
                t_clicklist_wl[pos]=int(info[10])
            
                
    #pdb.set_trace()
    detail_info=datanode(t_userid,
    t_utradeidfirst,t_utradeidsecond,t_orgidfirst,t_orgidsecond,t_orgidthird,t_firstconsumemonth,
    t_consumelist,t_clicklist,t_consumelist_wl,
    t_clicklist_wl)

    orgdata[t_userid]=detail_info

def obtain_result(forecastdate, currentdate, op, field, rrequest): #rrequest is an option saving for future
    loss_result={}    
    for op_i in op:
        for field_i in field:
            dp=op_i+'_'+field_i            
            loss_result[dp]=loss_rate(forecastdate, currentdate, op_i, field_i, rrequest)
    return(loss_result)
  
    
def loss_rate(forecastdate, currentdate,op, field,rrequest):
    
    stat_cus=[]
    ratio=[]
    earliest_date='2010-01'
    earliest_pos=getpos(earliest_date)
    forecast_pos=getpos(forecastdate)
    current_pos=getpos(currentdate)

    length=current_pos-earliest_pos+2
    ratio=[0 for n in range(0, length)]
    stat_cus=[]  #obtain the left customer for each orgin
    for i in range(0, length):
        b=[0 for n in range(0, length)]
        stat_cus.append(b)

    for key in orgdata.keys(): # deal each customer
        if (op=='all' or orgdata[key].orgidfirst==op) and (field=='all' or orgdata[key].utradeidfirst==field):
            begin_pos=getpos(orgdata[key].firstconsumemonth)
            if begin_pos<earliest_pos:
                begin_pos=earliest_pos-1  #for customer before 2010, handle together
            
            posit=begin_pos-earliest_pos+1
            stat_cus[posit][posit]+=1  #get the customer number at the beginning pos
            temp_n=current_pos
            while orgdata[key].pcconsume[temp_n]==0 and orgdata[key].wlconsume[temp_n]==0:
                temp_n=temp_n-1
            endit=temp_n-earliest_pos+1
            stat_cus[posit][endit]+=1 #get the customer number at the ending pos
        
    #pdb.set_trace()        
    for i in range(0, len(stat_cus)):
        for j in range(length-1,i+1,-1):
            stat_cus[i][j-1]=stat_cus[i][j-1]+stat_cus[i][j] # obtain the real num of each period
            
    distance=forecast_pos-current_pos
    for i in range(0, distance+1): # for very long-live customers
        if stat_cus[0][current_pos-earliest_pos+1-distance]!=0:
            ratio[i]=(float)(stat_cus[0][current_pos-earliest_pos+1])/stat_cus[0][current_pos-earliest_pos+1-distance]
        else:
            ratio[i]=0
        
    for i in range(distance+1, len(stat_cus)): # for the left customers

        temp_ratio=0
        temp_distance=current_pos-earliest_pos+1-i
	temp_n=0
        for j in range(1, i):
            if stat_cus[j][j+temp_distance]!=0:
		temp_n=temp_n+1
                temp_ratio=temp_ratio+(float)(stat_cus[j][j+temp_distance+distance])/stat_cus[j][j+temp_distance]
            else:
                temp_ratio=0
	if temp_n>0:
        	ratio[i]=temp_ratio/(temp_n)
	else:
		ratio[i]=0

    left_customer=0
    customer_num=0
    for i in range(0, length):
	customer_num=customer_num+stat_cus[i][current_pos-earliest_pos+1]
        left_customer+=stat_cus[i][current_pos-earliest_pos+1]*ratio[i]
    #pdb.set_trace()
    print(customer_num)
    return(left_customer)
    	
        
        
        
    

    
     
           
'''
if __name__=="__main__":
    readline()
    print("hello done") 	
    left_customer=obtain_result('2013-04','2013-03', ['zhixiao','qudao'],['16','32'],0)

    for key in left_customer.keys():
        print(key+'\t'+str(left_customer[key]))
    
   
 
    #pdb.set_trace()
    print('end')
'''
    
    
                
        
        
    

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
    filename=open("loss_charge_temp.txt")
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
  
    
def loss_rate(orgdate, currentdate):
    
    stat_cus={}
    
    for key in orgdata.keys():
        
        current_pos=getpos(currentdate)
        forecast_pos=getpos(orgdate)
        begin_pos=getpos(orgdata[key].firstconsumemonth)
        if begin_pos not in stat_cus:
        
            time_length=current_pos-begin_pos
            timelist=[0 for n in range(0,time_length+1)]
        temp_n=current_pos
        while orgdata[key].pcconsume[temp_n]==0 and orgdata[key].wlconsume[temp_n]==0:
            temp_n=temp_n-1
        stat_cus[begin_pos].timelist[temp_n-begin_pos]+=1
        
    

    
     
            

if __name__=="__main__":
    readline()
 
    #pdb.set_trace()
    print('end')

    
    
                
        
        
    

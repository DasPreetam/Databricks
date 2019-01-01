import json, dateutil.parser as parser, datetime, ast, glob

daysdict,tempdict,hoursdict={},{},{}
minuteslist,hourslist,dayslist=[],[],[]
totalRegRead,interRegRead=0,0

try :
  path= 'Data*.json'   
  files= glob.glob(path)

  for item in files:
    fileOp = open(item,'r')
    indata = ast.literal_eval(fileOp.read())
    fileOp.close()
    temp = (temp2['CurrentRegisterRead'] for temp2 in indata['days'])
    mainReading = next(temp)
    currdate=parser.parse(indata['UpDateTime'])

    data={x: indata[x] for x in indata if x not in 'days'}
    data['IntervalLength']=5
    fileOp = open("Percentage.csv",'r')
    for line in fileOp:
      hourslist,dayslist=[],[]
      totalRegRead,stepsize,minutesgap=0,12,5
      percentage=line.split(',')
      for columns in range(0,287,stepsize):
        interRegRead=0
        for innercol in range(columns,columns+stepsize):
          tempdict['date']="ISODate('"+currdate.isoformat()+".000Z')"
          tempdict['CurrentRegisterRead']=round((float(percentage[innercol])*mainReading/100),2)
          interRegRead+=tempdict['CurrentRegisterRead']
          minuteslist.append(tempdict.copy())
          currdate+=datetime.timedelta(hours=0,minutes=minutesgap)
    
        hoursdict['date']=minuteslist[0]['date']
        hoursdict['CurrentRegisterRead']=round(interRegRead,2)
        hoursdict['minutes']=minuteslist
        minuteslist=[]
        totalRegRead+=interRegRead
        hourslist.append(hoursdict.copy())
       
      daysdict['date']=data['date']
      daysdict['CurrentRegisterRead']=round(totalRegRead,2)
      daysdict['hours']=hourslist
      dayslist.append(daysdict)
      data['days']=dayslist

      with open(data['NMI']+"_"+data['UpDateTime'].replace('-','_')+".json", 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()
    
    fileOp.close()    

  print("Run Complete")
  input("Hit Return to exit")

except BaseException as e:
  print(str(e))
  input("Hit Return to exit")

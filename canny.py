
#import data from file
#filename = input('enter file name: ')
file = open('Lena256.raw','rb')
while 1:
    x=[]
    data = file.readline()
    if not data:
        break
    #data.split(str=" ", num=256)
    intData=bytes.decode(data)
    for i in range(0,len(intData),4):
        x.append(intData[i:i+4])
    print(x)




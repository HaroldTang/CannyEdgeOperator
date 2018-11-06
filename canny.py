import numpy as np
from PIL import Image


#import data from file
class CannyOperation():
    def canny(self,string):
        #filename = input('enter file name: ')
        rawData = Image.open(string) #openfile and read rawdata
        #rawData.show()
        i = rawData.size[1]          #get i
        j = rawData.size[0]          #get j
        print(i, j)
        dataList = [([0] * j) for x in range(i)]   #initial a double list based on size of picture.

        for x in range(j):
            for y in range(i):
                dataList[y][x] = rawData.getpixel((x, y))        #format rawdata into a double list

        formatData = np.array(dataList)
        print(formatData)

        GResult = self.gFilter(formatData)
        print(GResult)




    def gFilter( self, list ):
        self.list = list
        gaussianFilter = np.array(([ 1, 1, 2, 2, 2, 1, 1 ],
                                   [ 1, 2, 2, 4, 2, 2, 1 ],
                                   [ 2, 2, 4, 8, 4, 2, 2 ],
                                   [ 2, 4, 8,16, 8, 4, 2 ],
                                   [ 2, 2, 4, 8, 4, 2, 2 ],
                                   [ 1, 2, 2, 4, 2, 2, 1 ],
                                   [ 1, 1, 2, 2, 2, 1, 1 ]))
        i_new = len(list[ 0 ][ : ])-6
        j_new = len(list[ :, -1 ])-6
        #print(j_new, i_new)
        new_image = np.zeros((j_new,i_new), dtype=np.int)
        for a in range(j_new):
            for b in range(i_new):
                new_image[a,b] = np.sum(list[ a: a+7, b:b+7 ] * gaussianFilter)/140
        return new_image

    def prewitt( self, image ):
        return 0

Canny = CannyOperation()
Canny.canny("Lena256.bmp")
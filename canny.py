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
        #print(formatData)

        gResult = self.gFilter(formatData, i , j)
        #print(gResult)
        gradient= self.prewittOp(gResult, i , j)
        print(gradient)
        pic = Image.fromarray(gradient)
        pic.show()

    # def conv( self, image, i, j , weight, boundary):
    #     self.image = image
    #     self.i = i
    #     self.j = j
    #     self.weight = weight
    #     self.boundary = boundary
    #     i_new = len(image[0][:]) - boundary
    #     j_new = len(image[:,-1]) - boundary
    #     new_Image = np.zeros((i,j), dtype = np.float)
    #     for a in range(boundary, j_new):
    #         for b in range(boundary, i_new):
    #             new_Image[a,b] = np.sum(image[a-len(weight[0][:]): a+len(weight[0][:]) + 1, b-len(weight[0][:]):b+len(weight[0][:]) + 1] * weight)
    #     return new_Image

    def gFilter( self, image, i, j ):
        self.list = image
        self.i = i
        self.j = j
        gaussianFilter = np.array(([ 1, 1, 2, 2, 2, 1, 1 ],
                                   [ 1, 2, 2, 4, 2, 2, 1 ],
                                   [ 2, 2, 4, 8, 4, 2, 2 ],
                                   [ 2, 4, 8,16, 8, 4, 2 ],
                                   [ 2, 2, 4, 8, 4, 2, 2 ],
                                   [ 1, 2, 2, 4, 2, 2, 1 ],
                                   [ 1, 1, 2, 2, 2, 1, 1 ]))
        # gImage = self.conv(image, i, j, gaussianFilter, 3)
        # normalImage = gImage/140.0
        # return normalImage
        i_gau = len(image[ 0 ][ : ]) - 3
        j_gau = len(image[ :, -1 ]) - 3
        #print(j_gau, i_gau)
        gauImage = np.zeros((i, j), dtype=np.float)
        for a in range(3,j_gau):
            for b in range(3,i_gau):
                gauImage[a,b] = np.sum(image[ a - 3: a + 4, b - 3:b + 4 ] * gaussianFilter) / 140.0
        return gauImage

    def prewittOp( self, image, i, j):
        self.image = image
        self.i = i
        self.j = j
        i_pre = len(image[ 0 ][ : ]) - 4
        j_pre = len(image[ :, -1 ]) - 4
        prewitt_X = np.array(([ -1, 0, 1 ], [ -1, 0, 1 ], [ -1, 0, 1 ]))
        prewitt_Y = np.array(([ 1, 1, 1 ], [ 0, 0, 0 ], [ -1, -1, -1 ]))
        image_X= np.zeros((i, j), dtype=np.float)
        image_Y= np.zeros((i, j), dtype=np.float)
        image_gradient = np.zeros((i, j), dtype=np.float)

        for a in range(4,j_pre):
            for b in range(4,i_pre):
                image_X[a,b] = np.sum(image[ a-1 : a+2, b-1 : b+2 ] * prewitt_X )

        for x in range(4,j_pre):
            for y in range(4,i_pre):
                image_Y[x,y] = np.sum(image[ x-1 : x+2, y-1 : y+2 ] * prewitt_Y )

        for m in range(i):
            for n in range(j):
                image_gradient[m][n] =np.sqrt(np.square(image_X[m][n])+np.square(image_Y[m][n]))
        return image_gradient

Canny = CannyOperation()
Canny.canny("zebra-crossing-1.bmp")
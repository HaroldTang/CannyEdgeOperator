import math
import numpy as np
from PIL import Image


# import data from file
class CannyOperation:
    def canny( self, string ):
        # filename = input('enter file name: ')
        raw_data = Image.open(string)  # openfile and read rawdata
        # rawData.show()
        i = raw_data.size[ 1 ]  # get i
        j = raw_data.size[ 0 ]  # get j
        # print(i, j)
        data_list = [ ([ 0 ] * j) for x in range(i) ]  # initial a double list based on size of picture.

        for x in range(j):
            for y in range(i):
                data_list[ y ][ x ] = raw_data.getpixel((x, y))  # format rawdata into a double list

        format_data = np.array(data_list)
        # print(formatData)

        gau_result = self.gau_filter(format_data, i, j)  # use gaussian filter to convolute the picture

        gradient, angle = self.Prewitt_op(gau_result, i, j)  # use prewitt operator to detect the edge
        # pic = Image.fromarray(gradient)
        # pic.show()
        suppressed_image = self.nm_suppression(gradient, angle, i, j)
        print(suppressed_image)
        # pic = Image.fromarray(suppressed_image)
        # pic.show()

    # def conv( self, image, i, j , weight, boundary):        #use to encapsulate the convolution operation
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

    def gau_filter( self, image, i, j ):
        self.list = image
        self.i = i
        self.j = j

        gaussian_filter = np.array(([ 1, 1, 2, 2, 2, 1, 1 ],  # define gaussian filter
                                    [ 1, 2, 2, 4, 2, 2, 1 ],
                                    [ 2, 2, 4, 8, 4, 2, 2 ],
                                    [ 2, 4, 8, 16, 8, 4, 2 ],
                                    [ 2, 2, 4, 8, 4, 2, 2 ],
                                    [ 1, 2, 2, 4, 2, 2, 1 ],
                                    [ 1, 1, 2, 2, 2, 1, 1 ]))
        # gImage = self.conv(image, i, j, gaussianFilter, 3)
        # normalImage = gImage/140.0
        # return normalImage
        i_gau = len(image[ 0 ][ : ]) - 3  # get the variant of the loop
        j_gau = len(image[ :, -1 ]) - 3
        # print(j_gau, i_gau)
        gau_image = np.zeros((i, j), dtype=np.float)  # initialize an array contains of zero
        for a in range(3, j_gau):
            for b in range(3, i_gau):
                gau_image[ a, b ] = np.sum(image[ a - 3: a + 4,
                                           b - 3:b + 4 ] * gaussian_filter) / 140.0  # for each pixel that will be convoluted, use matrix multiplication to get result
        return gau_image

    def Prewitt_op( self, image, i, j ):
        self.image = image
        self.i = i
        self.j = j

        i_pre = len(image[ 0 ][ : ]) - 4  # get the variant of the loop
        j_pre = len(image[ :, -1 ]) - 4
        Prewitt_x = np.array(([ -1, 0, 1 ], [ -1, 0, 1 ], [ -1, 0, 1 ]))  # define prewitt X operator
        Prewitt_y = np.array(([ 1, 1, 1 ], [ 0, 0, 0 ], [ -1, -1, -1 ]))  # define prewitt Y operator
        image_x = np.zeros((i, j), dtype=np.float)
        image_y = np.zeros((i, j), dtype=np.float)
        image_gradient = np.zeros((i, j), dtype=np.float)  # create three empty matrix to store the value
        gradient_angle = np.zeros((i, j), dtype=np.float)

        for a in range(4, j_pre):
            for b in range(4, i_pre):
                image_x[ a, b ] = np.sum(image[ a - 1: a + 2, b - 1: b + 2 ] * Prewitt_x)

        for x in range(4, j_pre):
            for y in range(4, i_pre):
                image_y[ x, y ] = np.sum(image[ x - 1: x + 2, y - 1: y + 2 ] * Prewitt_y)

        for m in range(i):
            for n in range(j):
                image_gradient[ m ][ n ] = np.sqrt(
                    np.square(image_x[ m ][ n ]) + np.square(image_y[ m ][ n ]))  # get the gradient of each image
                gradient_angle[ m ][ n ] = math.degrees(np.arctan2(image_y[ m ][ n ], image_x[ m ][ n ]))
        return image_gradient, gradient_angle  # abs(image_x), abs(image_y)

    def nm_suppression( self, image, angle, i, j ):
        self.image = image
        self.angle = angle
        self.i = i
        self.j = j

        suppress_image = np.zeros((i, j), dtype=np.float)
        for x in range(5, (len(image[ :, -1 ]) - 5)):  # compare each pixel with surrounding pixels to thin the edge
            for y in range(5, (len(image[ 0 ][ : ]) - 5)):
                if (angle[ x ][ y ] < 22.5 or angle[ x ][ y ] >= 337.5) or (
                        angle[ x ][ y ] >= 157.5 and angle[ x ][ y ] < 202.5):  # label 0
                    if image[ x ][ y ] == max(image[ x ][ y ], image[ x - 1 ][ y ], image[ x + 1 ][ y ]):
                        suppress_image[ x ][ y ] = image[ x ][ y ]
                    else:
                        suppress_image[ x ][ y ] = 0
                elif (angle[ x ][ y ] < 67.5 and angle[ x ][ y ] >= 22.5) or (
                        angle[ x ][ y ] >= 202.5 and angle[ x ][ y ] < 247.5):  # label 1
                    if image[ x ][ y ] == max(image[ x ][ y ], image[ x - 1 ][ y + 1 ], image[ x + 1 ][ y - 1 ]):
                        suppress_image[ x ][ y ] = image[ x ][ y ]
                    else:
                        suppress_image[ x ][ y ] = 0
                elif (angle[ x ][ y ] < 112.5 and angle[ x ][ y ] >= 67.5) or (  # label 2
                        angle[ x ][ y ] >= 247.5 and angle[ x ][ y ] < 292.5):
                    if image[ x ][ y ] == max(image[ x ][ y ], image[ x ][ y + 1 ], image[ x ][ y - 1 ]):
                        suppress_image[ x ][ y ] = image[ x ][ y ]
                    else:
                        suppress_image[ x ][ y ] = 0
                elif (angle[ x ][ y ] < 157.5 and angle[ x ][ y ] >= 112.5) or (  # label 3
                        angle[ x ][ y ] >= 292.5 and angle[ x ][ y ] < 337.5):
                    if image[ x ][ y ] == max(image[ x ][ y ], image[ x - 1 ][ y - 1 ], image[ x + 1 ][ y + 1 ]):
                        suppress_image[ x ][ y ] = image[ x ][ y ]
                    else:
                        suppress_image[ x ][ y ] = 0
        return suppress_image

    # def p_tile( self, image, i, j ):





Canny = CannyOperation()
Canny.canny("Zebra-crossing-1.bmp")

import math
import os

import numpy as np
from PIL import Image


class CannyOperation:
    def __init__( self, string ):
        self.filename = string
        raw_data = Image.open(string)  # open file and read raw data

        i_len = raw_data.size[ 1 ]  # get i
        j_len = raw_data.size[ 0 ]  # get j

        self.i_len = i_len  # pass parameter to entire program
        self.j_len = j_len

        data_list = [ ([ 0 ] * j_len) for _ in range(i_len) ]  # initial a double list based on size of picture.

        for x in range(i_len):
            for y in range(j_len):
                data_list[ x ][ y ] = raw_data.getpixel((y, x))  # input raw data into a double list

        self.format_data = np.array(data_list)
        path = "./output"  # create dictionary for output
        if not os.path.exists(path):
            os.mkdir(path)

    def canny( self ):

        gau_result = self.gau_filter(self.format_data)  # use gaussian filter to convoluted picture
        out_gau = Image.fromarray(gau_result).convert("L")
        out_gau.save('./output/gaussian_' + self.filename)

        gradient, angle, pic_x, pic_y = self.Prewitt_op(gau_result)  # use Prewitt operator to detect the edge
        out_gradient = Image.fromarray(gradient).convert("L")
        out_gradient.save('./output/gradient_' + self.filename)

        out_x = Image.fromarray(pic_x).convert("L")  # output horizontal and vertical image
        out_x.save('./output/horizontal_' + self.filename)
        out_y = Image.fromarray(pic_y).convert("L")
        out_y.save('./output/vertical_' + self.filename)

        suppressed_image = self.nm_suppression(gradient, angle)  # use non-maxima suppression
        out_suppression = Image.fromarray(suppressed_image).convert("L")
        out_suppression.save('./output/non_maxima_' + self.filename)

        x10, edge_num10, final_image1 = self.p_tile(suppressed_image, 0.1)  # use p-tile method to set threshold
        x30, edge_num30, final_image3 = self.p_tile(suppressed_image, 0.3)
        x50, edge_num50, final_image5 = self.p_tile(suppressed_image, 0.5)

        f = open("./output/finalResult.txt", 'a')  # output result
        f.write(self.filename + " threshold for 10 percent is %d, total number of edges is %d\n" % (x10, edge_num10))
        f.write(self.filename + " threshold for 30 percent is %d, total number of edges is %d\n" % (x30, edge_num30))
        f.write(self.filename + " threshold for 50 percent is %d, total number of edges is %d\n" % (x50, edge_num50))
        f.close()

        pic1 = Image.fromarray(final_image1).convert("L")  # output the final image
        pic3 = Image.fromarray(final_image3).convert("L")
        pic5 = Image.fromarray(final_image5).convert("L")
        pic1.save('./output/10percent_' + self.filename)
        pic3.save('./output/30percent_' + self.filename)
        pic5.save('./output/50percent_' + self.filename)

    def conv( self, image, weight, boundary, former ):  # use to encapsulate the convolution operation

        i_new = self.i_len - boundary - former  # set new boundary for image
        j_new = self.j_len - boundary - former
        new_image = np.zeros((self.i_len, self.j_len), dtype=np.float)  # create matrix filled with 0.0
        for a in range(boundary + former, i_new):
            for b in range(boundary + former, j_new):
                new_image[ a ][ b ] = np.sum(
                    image[ a - boundary: a + boundary + 1,
                    b - boundary:b + boundary + 1 ] * weight)  # multiple two matrices to get convolution iteratively
        return new_image

    def gau_filter( self, image ):
        gaussian_filter = np.array(([ 1, 1, 2, 2, 2, 1, 1 ],  # define gaussian filter
                                    [ 1, 2, 2, 4, 2, 2, 1 ],
                                    [ 2, 2, 4, 8, 4, 2, 2 ],
                                    [ 2, 4, 8, 16, 8, 4, 2 ],
                                    [ 2, 2, 4, 8, 4, 2, 2 ],
                                    [ 1, 2, 2, 4, 2, 2, 1 ],
                                    [ 1, 1, 2, 2, 2, 1, 1 ]))
        gau_image = self.conv(image, gaussian_filter, 3, 0)  # convolution the image with gaussian filter to smooth it
        normal_image = gau_image / 140.0
        return normal_image

    def Prewitt_op( self, image ):

        Prewitt_x = np.array(([ -1, 0, 1 ],
                              [ -1, 0, 1 ],
                              [ -1, 0, 1 ]))  # define prewitt horizontal operator
        Prewitt_y = np.array(([ 1, 1, 1 ],
                              [ 0, 0, 0 ],
                              [ -1, -1, -1 ]))  # define prewitt vertical operator
        image_x = self.conv(image, Prewitt_x, 1, 3)
        image_y = self.conv(image, Prewitt_y, 1, 3)
        image_gradient = np.zeros((self.i_len, self.j_len),
                                  dtype=np.float)  # create two empty matrices to store the value
        gradient_angle = np.zeros((self.i_len, self.j_len), dtype=np.float)

        for m in range(self.i_len):
            for n in range(self.j_len):
                image_gradient[ m ][ n ] = np.sqrt(
                    np.square(image_x[ m ][ n ]) + np.square(image_y[ m ][ n ]))  # get the gradient for each pixel
                gradient_angle[ m ][ n ] = math.degrees(
                    np.arctan2(image_y[ m ][ n ], image_x[ m ][ n ]))  # get gradient angle for each pixel
        return image_gradient, gradient_angle, abs(image_x), abs(image_y)

    def nm_suppression( self, image, angle ):

        pixel1 = None
        pixel2 = None
        suppress_image = np.zeros((self.i_len, self.j_len), dtype=np.float)
        for x in range(4, self.i_len - 4):  # compare each pixel with surrounding pixels to thin the edge
            for y in range(4, self.j_len - 4):
                if abs(angle[ x ][ y ]) <= 22.5 or abs(angle[ x ][ y ]) > 157.5:  # label 0
                    pixel1 = image[ x ][ y + 1 ]
                    pixel2 = image[ x ][ y - 1 ]
                elif 22.5 <= angle[ x ][ y ] < 67.5 or -157.5 <= angle[ x ][ y ] < -112.5:  # label 1
                    pixel1 = image[ x + 1 ][ y - 1 ]
                    pixel2 = image[ x - 1 ][ y + 1 ]
                elif 67.5 <= angle[ x ][ y ] < 112.5 or -112.5 <= angle[ x ][ y ] < -67.5:  # label 2
                    pixel1 = image[ x + 1 ][ y ]
                    pixel2 = image[ x - 1 ][ y ]
                elif 112.5 <= angle[ x ][ y ] < 157.5 or -67.5 <= angle[ x ][ y ] < -22.5:  # label 3
                    pixel1 = image[ x - 1 ][ y - 1 ]
                    pixel2 = image[ x + 1 ][ y + 1 ]
                if image[ x ][ y ] == max(image[ x ][ y ], pixel1,
                                          pixel2):  # if greater than two neighbors, keep the value, otherwise set 0
                    suppress_image[ x ][ y ] = image[ x ][ y ]
                else:
                    suppress_image[ x ][ y ] = 0
        return suppress_image

    def p_tile( self, image, p ):
        threshold = 0
        final_image = np.zeros((self.i_len, self.j_len))

        threshold_sum = 0
        t = math.floor(np.max(image))  # get max pixel gradient

        count = [ 0 for _ in range(t + 1) ]  # set a new list to count total number of pixels in same gray level

        for x in range(self.i_len):
            for y in range(self.j_len):
                if int(image[ x ][ y ]) != 0:  # if pixel is not zero, add 1 to list in particular index
                    count[ int(image[ x ][ y ]) ] += 1

        right_sum = p * np.sum(count)  # set right part of total pixel number

        for i in range(t, 0, -1):
            threshold_sum += count[ i ]
            if threshold_sum >= right_sum:  # if i pixel in right part add up to threshold sum, then set the threshold at i
                threshold = i
                break

        for x in range(self.i_len):  # compare each pixel with threshold, if greater, set edge. Else set background
            for y in range(self.j_len):
                if image[ x ][ y ] >= threshold:
                    final_image[ x ][ y ] = 255
                else:
                    final_image[ x ][ y ] = 0

        pixel_count = np.count_nonzero(final_image == 255)
        return threshold, pixel_count, final_image


Canny = CannyOperation("Lena256.bmp")
Canny2 = CannyOperation("zebra-crossing-1.bmp")
Canny.canny()
Canny2.canny()

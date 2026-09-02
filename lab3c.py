import cv2
import matplotlib.pyplot as plt
import numpy as np


image=cv2.imread("./images/cat.jpg",cv2.IMREAD_GRAYSCALE)

image=cv2.resize(image,(512,512))


# Zero Padding
def zero_padding(image,pad):
    return np.pad(image,pad,mode='constant',constant_values=0)


# Apply Kernel
def apply_kernel(image,kernel):

    kernel=kernel[::-1,::-1]

    k=kernel.shape[0]//2

    padded=zero_padding(image,k)

    output=np.zeros(image.shape)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            region=padded[i:i+kernel.shape[0],
                          j:j+kernel.shape[1]]

            output[i,j]=np.sum(region*kernel)

    return output


# Gaussian Kernel
def gaussian_kernel(size,sigma):

    k=size//2

    kernel=np.zeros((size,size))

    for i in range(size):
        for j in range(size):

            x=i-k
            y=j-k

            kernel[i,j]=np.exp(-(x*x+y*y)/(2*sigma*sigma))

    kernel=kernel/kernel.sum()

    return kernel


# 1st Derivative of Gaussian X
def gaussian_dx_kernel(size,sigma):

    k=size//2

    kernel=np.zeros((size,size))

    for i in range(size):
        for j in range(size):

            x=i-k
            y=j-k

            g=np.exp(-(x*x+y*y)/(2*sigma*sigma))

            kernel[i,j]=-(x/(sigma*sigma))*g

    return kernel


# 1st Derivative of Gaussian Y
def gaussian_dy_kernel(size,sigma):

    k=size//2

    kernel=np.zeros((size,size))

    for i in range(size):
        for j in range(size):

            x=i-k
            y=j-k

            g=np.exp(-(x*x+y*y)/(2*sigma*sigma))

            kernel[i,j]=-(y/(sigma*sigma))*g

    return kernel


# LoG Kernel
def log_kernel(size,sigma):

    k=size//2

    kernel=np.zeros((size,size))

    for i in range(size):
        for j in range(size):

            x=i-k
            y=j-k

            r2=x*x+y*y

            kernel[i,j]=((r2-2*sigma*sigma)/(sigma**4))*np.exp(-r2/(2*sigma*sigma))

    return kernel


# Sobel X
def sobel_x_kernel():

    kernel=np.array([
        [-1,0,1],
        [-2,0,2],
        [-1,0,1]
    ])

    return kernel


# Sobel Y
def sobel_y_kernel():

    kernel=np.array([
        [-1,-2,-1],
        [ 0, 0, 0],
        [ 1, 2, 1]
    ])

    return kernel


# Custom Kernel
def custom_kernel():

    kernel=np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])

    return kernel


# Generate Kernels
kernel_gaussian=gaussian_kernel(5,2)

kernel_dx=gaussian_dx_kernel(5,1)

kernel_dy=gaussian_dy_kernel(5,1)

kernel_log=log_kernel(5,1)

kernel_sobel_x=sobel_x_kernel()

kernel_sobel_y=sobel_y_kernel()

kernel_custom=custom_kernel()


# Apply Filters
output_gaussian=apply_kernel(image,kernel_gaussian)

output_dx=apply_kernel(image,kernel_dx)

output_dy=apply_kernel(image,kernel_dy)

output_log=apply_kernel(image,kernel_log)

output_sobel_x=apply_kernel(image,kernel_sobel_x)

output_sobel_y=apply_kernel(image,kernel_sobel_y)

output_custom=apply_kernel(image,kernel_custom)


# Gaussian
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_gaussian,cmap="gray")
plt.title("Gaussian")
plt.axis("off")

plt.show()


# 1st Derivative X
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_dx,cmap="gray")
plt.title("1st Derivative Gaussian X")
plt.axis("off")

plt.show()


# 1st Derivative Y
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_dy,cmap="gray")
plt.title("1st Derivative Gaussian Y")
plt.axis("off")

plt.show()


# LoG
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_log,cmap="gray")
plt.title("LoG")
plt.axis("off")

plt.show()


# Sobel X
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_sobel_x,cmap="gray")
plt.title("Sobel X")
plt.axis("off")

plt.show()


# Sobel Y
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_sobel_y,cmap="gray")
plt.title("Sobel Y")
plt.axis("off")

plt.show()


# Custom
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_custom,cmap="gray")
plt.title("Custom Filter")
plt.axis("off")

plt.show()
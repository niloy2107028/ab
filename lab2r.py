import cv2
import matplotlib.pyplot as plt
import numpy as np

image=cv2.imread("./images/cat.jpg")

image=cv2.resize(image,(512,512))

# OpenCV reads image as BGR
b,g,r=cv2.split(image)

# B channel
hist_b=np.zeros(256)

for i in range(b.shape[0]):
    for j in range(b.shape[1]):
        hist_b[b[i][j]]+=1

mn=b.shape[0]*b.shape[1]

pdf_b=hist_b.copy()

for i in range(256):
    pdf_b[i]/=mn

cdf_b=np.zeros(256)
cdf_b[0]=pdf_b[0]

for i in range(1,256):
    cdf_b[i]=pdf_b[i]+cdf_b[i-1]

mapp_b={}

for i in range(256):
    mapp_b[i]=round(255*cdf_b[i])

new_b=b.copy()

for i in range(b.shape[0]):
    for j in range(b.shape[1]):
        new_b[i][j]=mapp_b[b[i][j]]


# G channel
hist_g=np.zeros(256)

for i in range(g.shape[0]):
    for j in range(g.shape[1]):
        hist_g[g[i][j]]+=1

pdf_g=hist_g.copy()

for i in range(256):
    pdf_g[i]/=mn

cdf_g=np.zeros(256)
cdf_g[0]=pdf_g[0]

for i in range(1,256):
    cdf_g[i]=pdf_g[i]+cdf_g[i-1]

mapp_g={}

for i in range(256):
    mapp_g[i]=round(255*cdf_g[i])

new_g=g.copy()

for i in range(g.shape[0]):
    for j in range(g.shape[1]):
        new_g[i][j]=mapp_g[g[i][j]]


# R channel
hist_r=np.zeros(256)

for i in range(r.shape[0]):
    for j in range(r.shape[1]):
        hist_r[r[i][j]]+=1

pdf_r=hist_r.copy()

for i in range(256):
    pdf_r[i]/=mn

cdf_r=np.zeros(256)
cdf_r[0]=pdf_r[0]

for i in range(1,256):
    cdf_r[i]=pdf_r[i]+cdf_r[i-1]

mapp_r={}

for i in range(256):
    mapp_r[i]=round(255*cdf_r[i])

new_r=r.copy()

for i in range(r.shape[0]):
    for j in range(r.shape[1]):
        new_r[i][j]=mapp_r[r[i][j]]


# Merge channels
new_image=cv2.merge([new_b,new_g,new_r])


# Original Image
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis("off")

# New Image
plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(new_image,cv2.COLOR_BGR2RGB))
plt.title("Histogram Equalization")
plt.axis("off")

plt.tight_layout()
plt.show()
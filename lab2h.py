import numpy as np
import cv2
import matplotlib.pyplot as plt

def hequlizer(c):

    h=np.zeros(256)

    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            h[c[i][j]]+=1

    mn=c.shape[0]*c.shape[1]
    p=h/mn

    cdf=np.zeros(256)
    cdf[0]=p[0]

    for i in range(1,256):
        cdf[i]=cdf[i-1]+p[i]

    m={}

    for i in range(256):
        m[i]=np.round(1023*cdf[i])

    nc=np.zeros(c.shape,dtype=np.uint16)

    for i in range(nc.shape[0]):
        for j in range(nc.shape[1]):
            nc[i][j]=m[c[i][j]]

    hnew=np.zeros(1024)

    for i in range(nc.shape[0]):
        for j in range(nc.shape[1]):
            hnew[nc[i][j]]+=1

    return nc,h,hnew


image=cv2.imread("./images/x.jpeg")
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

r,g,b=cv2.split(image)

r_new,r_h,r_n_h=hequlizer(r)
g_new,g_h,g_n_h=hequlizer(g)
b_new,b_h,b_n_h=hequlizer(b)

rgb_eq=cv2.merge([r_new,g_new,b_new])


hsv=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)

h,s,v=cv2.split(hsv)

v_new,v_h,v_n_h=hequlizer(v)

v8=np.round(v_new/1023*255).astype(np.uint8)

new_hsv=cv2.merge([h,s,v8])

hsv_rgb=cv2.cvtColor(new_hsv,cv2.COLOR_HSV2RGB)

hsv_eq=np.round(
    hsv_rgb.astype(np.float32)/255*1023
).astype(np.uint16)


rgb8=np.round(rgb_eq/1023*255).astype(np.uint8)

rgb_eq_hsv=cv2.cvtColor(rgb8,cv2.COLOR_RGB2HSV)

rgb_eq_v=rgb_eq_hsv[:,:,2]

rgb_eq_v=np.round(
    rgb_eq_v.astype(np.float32)/255*1023
).astype(np.uint16)

rgb_eq_v_h=np.zeros(1024)

for i in range(rgb_eq_v.shape[0]):
    for j in range(rgb_eq_v.shape[1]):
        rgb_eq_v_h[rgb_eq_v[i][j]]+=1


hr,hg,hb=cv2.split(hsv_eq)

hr_h=np.zeros(1024)
hg_h=np.zeros(1024)
hb_h=np.zeros(1024)

for i in range(hsv_eq.shape[0]):
    for j in range(hsv_eq.shape[1]):
        hr_h[hr[i][j]]+=1
        hg_h[hg[i][j]]+=1
        hb_h[hb[i][j]]+=1


plt.figure(figsize=(12,9))

plt.subplot(3,3,1)
plt.imshow(image)
plt.title("Original 8-bit")
plt.axis("off")

plt.subplot(3,3,2)
plt.plot(r_h,'r')
plt.plot(g_h,'g')
plt.plot(b_h,'b')
plt.title("Original 8-bit - RGB Histogram")
plt.xlim(0,255)

plt.subplot(3,3,3)
plt.plot(v_h,'b')
plt.title("Original 8-bit - V Histogram")
plt.xlim(0,255)

plt.subplot(3,3,4)
plt.imshow(rgb_eq/1023)
plt.title("RGB Equalized (10-bit)")
plt.axis("off")

plt.subplot(3,3,5)
plt.plot(r_n_h,'r')
plt.plot(g_n_h,'g')
plt.plot(b_n_h,'b')
plt.title("RGB Equalized (10-bit) - RGB Histogram")
plt.xlim(0,1023)

plt.subplot(3,3,6)
plt.plot(rgb_eq_v_h,'b')
plt.title("RGB Equalized (10-bit) - V Histogram")
plt.xlim(0,1023)

plt.subplot(3,3,7)
plt.imshow(hsv_eq/1023)
plt.title("HSV Equalized (10-bit)")
plt.axis("off")

plt.subplot(3,3,8)
plt.plot(hr_h,'r')
plt.plot(hg_h,'g')
plt.plot(hb_h,'b')
plt.title("HSV Equalized (10-bit) - RGB Histogram")
plt.xlim(0,1023)

plt.subplot(3,3,9)
plt.plot(v_n_h,'b')
plt.title("HSV Equalized (10-bit) - V Histogram")
plt.xlim(0,1023)

plt.tight_layout()

plt.savefig("result.png",dpi=300,bbox_inches="tight")

plt.show()
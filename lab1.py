import numpy as np
import cv2
import matplotlib.pyplot as plt

# log transform 

image=cv2.imread("./images/cat.jpg",cv2.IMREAD_GRAYSCALE)
print(image.shape[0])
print(image.shape[1])
image=cv2.resize(image,(512,512))

new_image_log=image.copy()
new_image_gamma=image.copy()
new_image_threshold=image.copy()
new_image_gamma=image.astype(np.float32)

c1=255/np.log(256)
c2=255
gamma=0.1

for i in range(image.shape[0]):
    for j in range(image.shape[1]):

        new_image_log[i][j]=c1*np.log(1+new_image_log[i][j])


        new_image_gamma[i][j]=new_image_gamma[i][j]/255
        new_image_gamma[i][j]=c2*(new_image_gamma[i][j]**gamma)

        if(new_image_threshold[i][j]>128):
            new_image_threshold[i][j]=255
        else:
            new_image_threshold[i][j]=0


            
new_image_gamma=new_image_gamma.astype(np.uint8)
        

plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.axis("off")
plt.title("original image")

plt.subplot(1,2,2)
plt.imshow(new_image_log,cmap="gray")
plt.axis("off")
plt.title("log image")

plt.show()

plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.axis("off")
plt.title("original image")

plt.subplot(1,2,2)
plt.imshow(new_image_gamma,cmap="gray")
plt.axis("off")
plt.title("gamma image")

plt.show()


plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.axis("off")
plt.title("original image")

plt.subplot(1,2,2)
plt.imshow(new_image_threshold,cmap="gray")
plt.axis("off")
plt.title("threshold image")

plt.show()




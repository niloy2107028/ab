import cv2
import numpy as np
from matplotlib import pyplot as plt


# Read Image
image=cv2.imread("./images/pnoise.jpg",0)


# Fourier Transform
def fourier_transform(image):

    ft=np.fft.fft2(image)

    ft_shift=np.fft.fftshift(ft)

    magnitude=np.abs(ft_shift)

    phase=np.angle(ft_shift)

    return ft_shift,magnitude,phase


# Gaussian Low Pass Filter
def gaussian_lowpass_filter(magnitude, sigma):

    rows,cols=magnitude.shape

    center_x=rows//2
    center_y=cols//2

    filter=np.zeros((rows,cols))

    for i in range(rows):
        for j in range(cols):

            x=i-center_x
            y=j-center_y

            filter[i,j]=np.exp(-(x*x+y*y)/(2*sigma*sigma))

    new_magnitude=magnitude*filter
    # we are keeping the low frequencies 

    return new_magnitude


# Notch Reject Filter
def notch_filter(magnitude,points):

    new_magnitude=magnitude.copy()

    for point in points:
        # its a list of pairs or points

        x=point[0]
        y=point[1]

        new_magnitude[x,y]=0

    return new_magnitude

def notch_filter_radius(magnitude,points,radius):

    new_magnitude=magnitude.copy()

    for point in points:

        x=point[0]
        y=point[1]

        for i in range(magnitude.shape[0]):
            for j in range(magnitude.shape[1]):

                distance=(i-x)*(i-x)+(j-y)*(j-y)

                if distance<=radius*radius:
                    new_magnitude[i,j]=0

    return new_magnitude


# Combine Magnitude and Phase
def combine_magnitude_phase(magnitude,phase):

    final_result=magnitude*np.exp(1j*phase)

    return final_result


# Inverse Fourier Transform
def inverse_fourier(final_result):

    result=np.fft.ifftshift(final_result)

    image_back=np.fft.ifft2(result)

    image_back=np.real(image_back)

    image_back=cv2.normalize(
        image_back,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
        dtype=cv2.CV_8U
    )

    return image_back


# Fourier Transform
ft_shift,magnitude,phase=fourier_transform(image)


# Gaussian Low Pass
magnitude_gaussian=gaussian_lowpass_filter(magnitude,30)

final_gaussian=combine_magnitude_phase(
    magnitude_gaussian,
    phase
)

output_gaussian=inverse_fourier(final_gaussian)


# Notch Reject
points=[
    (261,261),
    (251,251)
]

magnitude_notch=notch_filter(magnitude,points)

final_notch=combine_magnitude_phase(
    magnitude_notch,
    phase
)

output_notch=inverse_fourier(final_notch)


# Magnitude Spectrum for Display
magnitude_spectrum=20*np.log(magnitude+1)

magnitude_spectrum=cv2.normalize(
    magnitude_spectrum,
    None,
    0,
    255,
    cv2.NORM_MINMAX,
    dtype=cv2.CV_8U
)


# Original Image and Gaussian
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_gaussian,cmap="gray")
plt.title("Gaussian Low Pass")
plt.axis("off")

plt.show()


# Original Image and Notch
plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(output_notch,cmap="gray")
plt.title("Notch Reject")
plt.axis("off")

plt.show()


# Magnitude Spectrum
plt.imshow(magnitude_spectrum,cmap="gray")
plt.title("Magnitude Spectrum")
plt.axis("off")

plt.show()



# Gaussian Low-Pass Filter (GLPF)

# filter[i,j]=np.exp(-(x*x+y*y)/(2*sigma*sigma))


# Gaussian High-Pass Filter (GHPF)

# filter[i,j]=1-np.exp(-(x*x+y*y)/(2*sigma*sigma))


# Gaussian Band-Reject Filter (GBRF)

# D=np.sqrt(x*x+y*y)
# filter[i,j]=1-np.exp(-((D*D-D0*D0)/(2*sigma*sigma*D)))


# Gaussian Notch-Reject Filter (GNRF)

# D=np.sqrt((i-x1)*(i-x1)+(j-y1)*(j-y1))
# filter[i,j]=1-np.exp(-(D*D)/(2*sigma*sigma))


# Gaussian Notch-Reject Filter (Two Symmetric Notches)

# D1=np.sqrt((i-x1)*(i-x1)+(j-y1)*(j-y1))
# D2=np.sqrt((i-x2)*(i-x2)+(j-y2)*(j-y2))

# filter[i,j]=(1-np.exp(-(D1*D1)/(2*sigma*sigma))) * \
#             (1-np.exp(-(D2*D2)/(2*sigma*sigma)))


# Butterworth Low-Pass Filter (BLPF)

# D=np.sqrt(x*x+y*y)
# filter[i,j]=1/(1+(D/D0)**(2*n))


# Butterworth High-Pass Filter (BHPF)

# D=np.sqrt(x*x+y*y)
# filter[i,j]=1/(1+(D0/D)**(2*n))


# Butterworth Band-Reject Filter (BBRF)

# D=np.sqrt(x*x+y*y)
# filter[i,j]=1/(1+((D*D-D0*D0)/(D*(D2-D1)))**(2*n))


# Butterworth Notch-Reject Filter (BNRF)

# D1=np.sqrt((i-x1)*(i-x1)+(j-y1)*(j-y1))
# D2=np.sqrt((i-x2)*(i-x2)+(j-y2)*(j-y2))

# filter[i,j]=1/(1+(D0*D0/(D1*D2))**(2*n))
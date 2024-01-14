import cv2
import numpy as np
import imghdr
import os

# Specify the folder path and image extensions
folder_path = 'media'
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

# List all files in the directory
all_files = os.listdir(folder_path)

# Filter only files with image extensions
image_files = [f for f in all_files if any(f.lower().endswith(ext) for ext in image_extensions)]

# Create full paths for image files
image_paths = [os.path.join(folder_path, f) for f in image_files]

# Get the latest image based on modification time
latest_image_path = max(image_paths, key=os.path.getmtime, default=None)

if latest_image_path:
    print(f"The latest image is: {latest_image_path}")
# else:
#     print("No image files found in the specified folder.")

    def get_illumination_channel(I, w):
        M, N, _ = I.shape
        padded = np.pad(I, ((int(w/2), int(w/2)), (int(w/2), int(w/2)), (0, 0)), 'edge')
        darkch = np.zeros((M, N))
        brightch = np.zeros((M, N))
        
        for i, j in np.ndindex(darkch.shape):
            darkch[i, j]  =  np.min(padded[i:i + w, j:j + w, :])
            brightch[i, j] = np.max(padded[i:i + w, j:j + w, :])
        
        return darkch, brightch

    def get_atmosphere(I, brightch, p=0.1):
        M, N = brightch.shape
        flatI = I.reshape(M*N, 3)
        flatbright = brightch.ravel()
        
        searchidx = (-flatbright).argsort()[:int(M*N*p)]  
        # find top M * N * p indexes. argsort() returns sorted (ascending) index.
        
        A = np.mean(flatI.take(searchidx, axis=0),dtype=np.float64, axis=0)

    def get_initial_transmission(A, brightch):
            A_c = np.max(A)
            init_t = (brightch-A_c)/(1.-A_c)
            return (init_t - np.min(init_t))/(np.max(init_t) - np.min(init_t))
    def get_corrected_transmission(I, A, darkch, brightch, init_t, alpha, omega, w):
        im3 = np.empty(I.shape, I.dtype);
        for ind in range(0,3):
            im3[:,:,ind] = I[:,:,ind]/A[ind]
            dark_c, _ = get_illumination_channel(im3, w)
            dark_t = 1 - omega*dark_c
            corrected_t = init_t
            diffch = brightch - darkch
        
        for i in range(diffch.shape[0]):
            for j in range(diffch.shape[1]):
                if(diffch[i,j]<alpha):
                    corrected_t[i,j] = dark_t[i,j]*init_t[i,j]
                        
        return np.abs(corrected_t)

    def get_final_image(I, A, corrected_t, tmin):
        corrected_t_broadcasted = np.broadcast_to(corrected_t[:,:,None], (corrected_t.shape[0], corrected_t.shape[1], 3))
        J = (I-A)/(np.where(corrected_t_broadcasted < tmin, tmin, corrected_t_broadcasted)) + A
        
        return (J - np.min(J))/(np.max(J) - np.min(J))

    # Load your source image

    source_image = cv2.imread(latest_image_path)
    # source_image = cv2.imread('c:/Users/Ahmad/Pictures/Camera Roll/WIN_20231030_10_10_18_Pro.jpg')

    # Create an empty image for the output
    output_image = cv2.detailEnhance(source_image)

    # Display or save the output_image
    cv2.imshow('Output Image', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




                                
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, EditProfileForm
from django.http import HttpResponse
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import Image
from .forms import ImageForm

# image illumination
import cv2
import numpy as np
import imghdr

import os

# from PIL import Image
import pytesseract as pt


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data.get("username")
                upass = fm.cleaned_data.get("password")
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Loged in successfully 🎉")
                    return HttpResponseRedirect("/profile/")

        else:
            fm = AuthenticationForm()
        return render(
            request,
            "ocrapp/login.html",
            {
                "form": fm,
            },
        )
    else:
        return HttpResponseRedirect("/profile/")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "ocrapp/profile.html", {"name": request.user})
    else:
        return HttpResponseRedirect("/login/")


def upload_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        form = ImageForm()
        img = Image.objects.all()
        return render(request, "ocrapp/upload.html", {"img": img, "form": form})
    else:
        return HttpResponseRedirect("/login/")


def signup_page(request):
    if request.POST:
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "User Created ")
            return HttpResponseRedirect("/")
    else:
        fm = SignupForm()
    return render(request, "ocrapp/register.html", {"form": fm})


from .forms import ImageForm

imgpath = None


def home(request):
    if request.POST:
        fm = ImageForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
    fm = ImageForm()
    img = Image.objects.all()
    global imgpath
    imgpath = Image.objects.last()
    return render(request, "home.html", {"img": img, "form": fm})


from .forms import ImageForm

imgpath = None


def dark_img_save(request):
    if request.POST:
        fm = ImageForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
    fm = ImageForm()
    img = Image.objects.all()
    global imgpath
    imgpath = Image.objects.last()
    return render(request, "dark_color_remove.html", {"img": img, "form": fm})


from django.http import HttpResponse
import os
from django.http import HttpResponse
from pathlib import Path

import pytesseract as pt


def show_result(request):
    import os
    import cv2
    from PIL import Image
    import pytesseract as pt

    # Assuming 'file_path' is the base directory
    file_path = "media\myimages"
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    # List all files in the directory
    all_files = os.listdir(file_path)

    # Filter only files with image extensions
    image_files = [
        f for f in all_files if any(f.lower().endswith(ext) for ext in image_extensions)
    ]

    # Create full paths for image files
    image_paths = [os.path.join(file_path, f) for f in image_files]

    # Get the latest image based on modification time
    latest_image_path = max(image_paths, key=os.path.getmtime, default=None)

    if latest_image_path:
        print(f"The latest image is: {latest_image_path}")
        # Use the latest image path for further processing

        # Your existing code for processing the latest image
        def show_image(img_path, size=(500, 500)):
            image = cv2.imread(img_path)
            image = cv2.resize(image, size)
            cv2.imshow("IMAGE", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # pt.pytesseract.tesseract_cmd = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
        # pt.pytesseract.tesseract_cmd = r"..\\.\\tesser\\tesseract.exe"
        # pt.pytesseract.tesseract_cmd = r"..\\.\\tesser\\tesseract.exe"
        # pt.pytesseract.tesseract_cmd = r"D:\\temp\\latest_Code_three\\tesser\\tesseract.exe"
        venv_path = Path('tesser/tesseract.exe')
        print(venv_path)
        pt.pytesseract.tesseract_cmd = venv_path 

        img = Image.open(latest_image_path)
        text = pt.image_to_string(img)
        print("-----------------img text-------------------")
        print(latest_image_path)
        print(text)
        print(imgpath)
        return render(request, "upload.html", {"text": text, "imagepath": imgpath})
        # return HttpResponse(text)

    else:
        return HttpResponse("No image files found in the specified directory.")


def bright_image(request):
    import cv2
    import numpy as np
    import os

    # Specify the folder path and image extensions
    folder_path = "media/myimages"
    output_folder = "output"  # Specify the output folder
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

    # List all files in the directory
    all_files = os.listdir(folder_path)

    # Filter only files with image extensions
    image_files = [
        f for f in all_files if any(f.lower().endswith(ext) for ext in image_extensions)
    ]

    # Create full paths for image files
    image_paths = [os.path.join(folder_path, f) for f in image_files]

    # Get the latest image based on modification time
    latest_image_path = max(image_paths, key=os.path.getmtime, default=None)

    if latest_image_path:
        print(f"The latest image is: {latest_image_path}")

        def get_illumination_channel(I, w):
            M, N, _ = I.shape
            padded = np.pad(
                I, ((int(w / 2), int(w / 2)), (int(w / 2), int(w / 2)), (0, 0)), "edge"
            )
            darkch = np.zeros((M, N))
            brightch = np.zeros((M, N))

            for i, j in np.ndindex(darkch.shape):
                darkch[i, j] = np.min(padded[i : i + w, j : j + w, :])
                brightch[i, j] = np.max(padded[i : i + w, j : j + w, :])

            return darkch, brightch

        def get_atmosphere(I, brightch, p=0.1):
            M, N = brightch.shape
            flatI = I.reshape(M * N, 3)
            flatbright = brightch.ravel()

            searchidx = (-flatbright).argsort()[: int(M * N * p)]
            A = np.mean(flatI.take(searchidx, axis=0), dtype=np.float64, axis=0)
            return A

        def get_initial_transmission(A, brightch):
            A_c = np.max(A)
            init_t = (brightch - A_c) / (1.0 - A_c)
            return (init_t - np.min(init_t)) / (np.max(init_t) - np.min(init_t))

        def get_corrected_transmission(I, A, darkch, brightch, init_t, alpha, omega, w):
            im3 = np.empty(I.shape, I.dtype)
            for ind in range(0, 3):
                im3[:, :, ind] = I[:, :, ind] / A[ind]
            dark_c, _ = get_illumination_channel(im3, w)
            dark_t = 1 - omega * dark_c
            corrected_t = init_t
            diffch = brightch - darkch

            for i in range(diffch.shape[0]):
                for j in range(diffch.shape[1]):
                    if diffch[i, j] < alpha:
                        corrected_t[i, j] = dark_t[i, j] * init_t[i, j]

            return np.abs(corrected_t)

        def get_final_image(I, A, corrected_t, tmin):
            corrected_t_broadcasted = np.broadcast_to(
                corrected_t[:, :, None], (corrected_t.shape[0], corrected_t.shape[1], 3)
            )
            J = (I - A) / (
                np.where(corrected_t_broadcasted < tmin, tmin, corrected_t_broadcasted)
            ) + A
            return (J - np.min(J)) / (np.max(J) - np.min(J))

        # Load your source image
        source_image = cv2.imread(latest_image_path)

        # Apply your image processing
        w = 15
        darkch, brightch = get_illumination_channel(source_image, w)
        A = get_atmosphere(source_image, brightch)
        init_t = get_initial_transmission(A, brightch)
        alpha = 0.1
        omega = 0.95
        corrected_t = get_corrected_transmission(
            source_image, A, darkch, brightch, init_t, alpha, omega, w
        )
        tmin = 0.1
        output_image = get_final_image(source_image, A, corrected_t, tmin)

        # Save the output image to the output folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(
            output_folder, f"output_{os.path.basename(latest_image_path)}.jpg"
        )
        cv2.imwrite(output_path, output_image * 255)

        print(f"Processed image saved at: {output_path}")
        import os
        import cv2
        from PIL import Image
        import pytesseract as pt

        # Assuming 'file_path' is the base directory
        file_path = "output"
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

        # List all files in the directory
        all_files = os.listdir(file_path)

        # Filter only files with image extensions
        image_files = [
            f
            for f in all_files
            if any(f.lower().endswith(ext) for ext in image_extensions)
        ]

        # Create full paths for image files
        image_paths = [os.path.join(file_path, f) for f in image_files]

        # Get the latest image based on modification time
        latest_image_path = max(image_paths, key=os.path.getmtime, default=None)

        if latest_image_path:
            print(f"The latest image is: {latest_image_path}")
            # Use the latest image path for further processing

            # Your existing code for processing the latest image
            def show_image(img_path, size=(500, 500)):
                image = cv2.imread(img_path)
                image = cv2.resize(image, size)
                cv2.imshow("IMAGE", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # pt.pytesseract.tesseract_cmd = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
            # pt.pytesseract.tesseract_cmd = r"..\\.\\tesser\\tesseract.exe"
            # pt.pytesseract.tesseract_cmd = r"D:\\temp\\latest_Code_three\\tesser\\tesseract.exe"
            venv_path = Path('tesser/tesseract.exe')
            pt.pytesseract.tesseract_cmd = venv_path 
            

            img = Image.open(latest_image_path)
            text = pt.image_to_string(img)
            print("-----------------img text-------------------")
            print(latest_image_path)
            print(text)
            print(imgpath)
            return render(request, "upload.html", {"text": text, "imagepath": imgpath})
    #            text = 'hi i am here'
    # return render(request, 'upload.html',{"text":text, 'imagepath':'/media/myimages/urdu.jpg'})

    # return HttpResponse(text)

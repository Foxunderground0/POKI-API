import hashlib
import os
import cv2

# prints all available algorithms
print("The available algorithms are : ", end="")
print(hashlib.algorithms_available)
os.chdir("Immages\sorted")
files = os.listdir(".")
print(files)
for file in files:
    f = open(file, "rb")
    immage = cv2.imread(file)
    if immage is None:
        f.close()
        os.remove(file)
    else:
        bytes = f.read()  # read entire file as bytes
        f.close()
        extension = os.path.splitext(file)[1]
        emotion = file.split("_")[0]
        if (emotion == "None"):
            os.remove(file)
        else:
            readable_hash = hashlib.sha256(bytes).hexdigest()
            print(readable_hash)

            try:
                os.rename(file, emotion + "_" + readable_hash + extension)
            except:
                os.remove(file)

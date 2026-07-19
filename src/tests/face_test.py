from deepface import DeepFace

# Replace with your image file names
img1_path = "person1.jpg"
img2_path = "person2.jpg"

result = DeepFace.verify(img1_path, img2_path)

print("Is same person?", result["verified"])

import os
from PIL import Image
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# TODO - receive file from front end and put it through the model

# standardize the images
def standardize_image(img, target_color=(0, 0, 0), target_size=(224, 224)):
    # Standardizes the image by setting a common color and resizing to a common size
    width, height = img.size

    # Color standardization
    if target_color != img.getpixel((0, 0)):  # Check if already desired color
        for i in range(width):
            for j in range(height):
                img.putpixel((i, j), target_color)

    # Size standardization
    if target_size != (width, height):
        img = img.resize(target_size, Image.LANCZOS)

    return img

# train healthy images
def healthyTraining(folder_path):
    sortedHealthy = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".PNG"):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    # Standardize the image
                    img_standardized = standardize_image(img)
                    sortedHealthy.append(img_standardized)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return sortedHealthy

# train broken images
def brokenTraining(folder_path):
    sortedBroken = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".PNG"):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    # Standardize the image
                    img_standardized = standardize_image(img)
                    sortedBroken.append(img_standardized)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    return sortedBroken

# TRAIN ALGORITHM TO CLASSIFY ALL IMAGES WITHOUT LABELS - TO BE DONE AFTER HEALTHY AND BROKEN LABELLING IS DONE
def algo(healthy_images, broken_images):
    # Prepares data and suggests potential algorithms

    # Combine images and labels
    training_images = healthy_images + broken_images
    training_labels = ["healthy"] * len(healthy_images) + ["broken"] * len(broken_images)

    # Feature extraction (example using raw pixel values)
    feature_vectors = []
    for image in training_images:
        # Convert image to a flat feature vector (e.g., a list of pixel values)
        feature_vector = np.array(image).flatten()  # Flatten the image
        feature_vectors.append(feature_vector)

    # Store data for later classification
    global training_data  # Declare as global for accessibility
    training_data = (feature_vectors, training_labels)

    # Suggest potential algorithms
    print("Consider exploring these algorithms:")
    print("- Decision trees")

    #Algorithm

    # Extract features and labels
    feature_vectors, training_labels = training_data

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(feature_vectors, training_labels, test_size=0.2, random_state=42)

    # Initialize the decision tree classifier
    clf = DecisionTreeClassifier()

    # Train the classifier
    clf.fit(X_train, y_train)

    # Predict on the testing set
    y_pred = clf.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy*100,"%")

    # TODO - SEND OR SHOW RESULT - WHICHEVER IS EASIER

if __name__ == "__main__":
    # access folder
    healthy_folder = "/Users/Ryan/Documents/Uni/testproject/templates/ML-Model/Healthy"  # Specify the Healthy folder path
    broken_folder = "/Users/Ryan/Documents/Uni/testproject/templates/ML-Model/Healthy"  # Specify the Broken folder path

    # sort images
    healthyArr = healthyTraining(healthy_folder)
    brokenArr = brokenTraining(broken_folder)

    # call main algo with healthy and broken arrays
    algo(healthyArr, brokenArr)

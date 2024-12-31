import os
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

TRAIN_DIR = 'backend/static/images/train'
TEST_DIR = 'backend/static/images/test'
MODEL_DIR = 'backend/model'
MODEL_PATH = os.path.join(MODEL_DIR, 'cataract_model.h5')

os.makedirs(MODEL_DIR, exist_ok=True)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    shuffle=False  
)

model.fit(train_generator, epochs=10, validation_data=validation_generator)

model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

predictions = model.predict(test_generator)
predicted_labels = (predictions > 0.5).astype(int)  

class_indices = {v: k for k, v in test_generator.class_indices.items()}  
predicted_class_names = [class_indices[label] for label in predicted_labels.flatten()]

for file, pred, label in zip(test_generator.filenames, predicted_class_names, test_generator.labels):
    true_class = class_indices[label]
    print(f"File: {file}, Predicted: {pred}, True: {true_class}")

def plot_predictions(generator, predictions, class_indices):
    class_names = {v: k for k, v in class_indices.items()}
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    axes = axes.flatten()

    for img, pred, label, ax in zip(generator[0][0], predictions, generator.labels, axes):
        ax.imshow(img)
        pred_label = class_names[int(pred > 0.5)]
        true_label = class_names[int(label)]
        ax.set_title(f"Pred: {pred_label}, True: {true_label}")
        ax.axis('off')

    plt.tight_layout()
    plt.show()

plot_predictions(test_generator, predictions, test_generator.class_indices)

y_true = test_generator.labels 
y_pred = (predictions > 0.5).astype(int) 

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=class_indices.values()))

import tensorflow as tf
import numpy as np
import cv2
import pygame
import sys
import time

# Initialize Pygame
pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("🎯 Teachable Machine - Detection UI")

font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

# Load model
model = tf.keras.models.load_model("keras_model.h5", compile=False)

# Load labels
with open("labels.txt", "r") as f:
    class_names = [line.strip()[2:] for line in f.readlines()]

# Camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Box UI layout
box_width = 200
box_height = 50
box_margin = 10
start_y = 100

box_positions = [
    pygame.Rect(550, start_y + i * (box_height +
                box_margin), box_width, box_height)
    for i in range(len(class_names))
]


def get_prediction(frame):
    image = cv2.resize(frame, (224, 224))
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    prediction = model.predict(image, verbose=0)
    index = np.argmax(prediction)
    return index, class_names[index], prediction[0][index]


# Blink timer
blink_state = True
last_blink_time = time.time()

# Main loop
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        print("Webcam not available.")
        break

    frame = cv2.flip(frame, 1)
    prediction_index, class_name, confidence = get_prediction(frame)

    # Convert OpenCV to pygame surface
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    frame_surface = pygame.transform.scale(frame_surface, (520, 390))

    # Blink logic (toggle every 0.5s)
    if time.time() - last_blink_time > 0.5:
        blink_state = not blink_state
        last_blink_time = time.time()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # Dark background
    screen.blit(frame_surface, (10, 100))

    # Display class boxes
    for i, box in enumerate(box_positions):
        color = (255, 255, 255)  # Default: white
        if i == prediction_index and blink_state:
            color = (0, 255, 0)  # Blink green
        pygame.draw.rect(screen, color, box, 3)
        label_surface = font.render(class_names[i], True, color)
        screen.blit(label_surface, (box.x + 10, box.y + 10))

    # Show prediction score
    pred_text = f"Detected: {class_name} ({confidence * 100:.2f}%)"
    pred_surface = font.render(pred_text, True, (0, 255, 0))
    screen.blit(pred_surface, (10, 20))

    pygame.display.update()
    clock.tick(30)

# Cleanup
cap.release()
pygame.quit()
sys.exit()

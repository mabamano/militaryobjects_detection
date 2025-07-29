import tensorflow as tf
import numpy as np
import cv2
import pygame
import sys
import time
import math
import textwrap

# Initialize Pygame
pygame.init()
window_size = (1200, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("TACTICAL AI RECONNAISSANCE SYSTEM")

# Fonts
title_font = pygame.font.SysFont("Arial", 28, bold=True)
main_font = pygame.font.SysFont("Arial", 36, bold=True)
sub_font = pygame.font.SysFont("Arial", 18)
spec_font = pygame.font.SysFont("Consolas", 11)
status_font = pygame.font.SysFont("Arial", 16, bold=True)
fps_font = pygame.font.SysFont("Arial", 14)
clock = pygame.time.Clock()

# Load model
model = tf.keras.models.load_model("keras_model.h5", compile=False)

# Load labels
with open("labels.txt", "r") as f:
    class_names = [line.strip()[2:] for line in f.readlines()]

# Camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Military color scheme
MILITARY_GREEN = (34, 51, 34)
MILITARY_DARK = (20, 30, 20)
MILITARY_LIGHT = (60, 80, 60)
MILITARY_ACCENT = (0, 255, 0)
MILITARY_WARNING = (255, 165, 0)
MILITARY_TEXT = (200, 255, 200)
MILITARY_BORDER = (0, 200, 0)

# Class specifications (mock data for military theme)
class_specs = {
    "missile": {
        "threat_level": "HIGH",
        "classification": "GUIDED WEAPON",
        "tactical_value": "STRATEGIC",
        "recommendation": "INTERCEPT IMMEDIATELY",
        "description": "Long-range, self-propelled guided weapon designed for precision strikes.",
        "dimensions": "4-7m LENGTH",
        "weight": "500-2000kg",
        "material": "ALLOY/COMPOSITE",
        "detection_range": "10-200km",
        "mobility": "AERIAL/LAUNCHED",
        "thermal_signature": "HIGH",
        "radar_cross_section": "MEDIUM",
        "threat_assessment": "SEVERE - IMMEDIATE RESPONSE REQUIRED",
        "countermeasures": "ANTI-MISSILE SYSTEMS",
        "intel_value": "HIGH - ENEMY CAPABILITY",
        "operational_impact": "CRITICAL"
    },
    "tanks": {
        "threat_level": "HIGH",
        "classification": "ARMORED VEHICLE",
        "tactical_value": "GROUND DOMINANCE",
        "recommendation": "DEPLOY ANTI-ARMOR",
        "description": "Heavily armored tracked vehicle with powerful main gun.",
        "dimensions": "6-10m LENGTH",
        "weight": "40-70t",
        "material": "ARMORED STEEL",
        "detection_range": "2-10km",
        "mobility": "TRACKED",
        "thermal_signature": "HIGH",
        "radar_cross_section": "LARGE",
        "threat_assessment": "HIGH - PRIORITY TARGET",
        "countermeasures": "ATGM/MINES/AIR SUPPORT",
        "intel_value": "HIGH - FORCE COMPOSITION",
        "operational_impact": "SIGNIFICANT"
    },
    "jets": {
        "threat_level": "HIGH",
        "classification": "FIGHTER AIRCRAFT",
        "tactical_value": "AIR SUPERIORITY",
        "recommendation": "ACTIVATE AIR DEFENSE",
        "description": "High-speed, maneuverable military aircraft for air-to-air combat.",
        "dimensions": "15-20m LENGTH",
        "weight": "10-30t",
        "material": "ALUMINUM/TITANIUM",
        "detection_range": "20-300km",
        "mobility": "AERIAL",
        "thermal_signature": "VERY HIGH",
        "radar_cross_section": "VARIABLE",
        "threat_assessment": "SEVERE - AIRSPACE VIOLATION",
        "countermeasures": "SAM/INTERCEPTORS",
        "intel_value": "HIGH - AIR ACTIVITY",
        "operational_impact": "CRITICAL"
    },
    "drones": {
        "threat_level": "MEDIUM",
        "classification": "UAV",
        "tactical_value": "RECON/STRIKE",
        "recommendation": "JAM/INTERCEPT",
        "description": "Unmanned aerial vehicle for surveillance or light attack.",
        "dimensions": "1-10m SPAN",
        "weight": "5-500kg",
        "material": "COMPOSITE",
        "detection_range": "1-50km",
        "mobility": "AERIAL",
        "thermal_signature": "LOW-MEDIUM",
        "radar_cross_section": "SMALL",
        "threat_assessment": "MODERATE - MONITOR CLOSELY",
        "countermeasures": "JAMMING/SHOOTDOWN",
        "intel_value": "MODERATE - ISR",
        "operational_impact": "TACTICAL"
    },
    "b2 bomber": {
        "threat_level": "HIGH",
        "classification": "STEALTH BOMBER",
        "tactical_value": "STRATEGIC STRIKE",
        "recommendation": "MAX ALERT",
        "description": "Long-range, low-observable heavy bomber for strategic missions.",
        "dimensions": "21m LENGTH, 52m WINGSPAN",
        "weight": "70t",
        "material": "COMPOSITE/STEALTH",
        "detection_range": "VARIABLE",
        "mobility": "AERIAL",
        "thermal_signature": "LOW",
        "radar_cross_section": "VERY LOW",
        "threat_assessment": "SEVERE - STRATEGIC THREAT",
        "countermeasures": "ADVANCED RADAR/SAM",
        "intel_value": "VERY HIGH - STRATEGIC",
        "operational_impact": "CRITICAL"
    },
    "nothing": {
        "threat_level": "NONE",
        "classification": "NO TARGET",
        "tactical_value": "NONE",
        "recommendation": "STANDBY",
        "description": "No object of interest detected in the field of view.",
        "dimensions": "N/A",
        "weight": "N/A",
        "material": "N/A",
        "detection_range": "N/A",
        "mobility": "N/A",
        "thermal_signature": "N/A",
        "radar_cross_section": "N/A",
        "threat_assessment": "NONE",
        "countermeasures": "NONE",
        "intel_value": "NONE",
        "operational_impact": "NONE"
    }
}


def draw_military_background(surface):
    """Draw military-style background with tactical elements."""
    # Main background
    surface.fill(MILITARY_DARK)

    # Header bar
    header_rect = pygame.Rect(0, 0, surface.get_width(), 60)
    pygame.draw.rect(surface, MILITARY_GREEN, header_rect)
    pygame.draw.line(surface, MILITARY_ACCENT, (0, 60),
                     (surface.get_width(), 60), 2)

    # Tactical grid pattern (subtle)
    for x in range(0, surface.get_width(), 50):
        pygame.draw.line(surface, MILITARY_LIGHT, (x, 0),
                         (x, surface.get_height()), 1)
    for y in range(0, surface.get_height(), 50):
        pygame.draw.line(surface, MILITARY_LIGHT, (0, y),
                         (surface.get_width(), y), 1)


def draw_military_panel(surface, rect, title, color=MILITARY_GREEN):
    """Draw a military-style panel with border and title."""
    # Panel background
    pygame.draw.rect(surface, color, rect, border_radius=5)
    pygame.draw.rect(surface, MILITARY_ACCENT, rect, width=2, border_radius=5)

    # Title bar
    title_rect = pygame.Rect(rect.x, rect.y, rect.width, 30)
    pygame.draw.rect(surface, MILITARY_DARK, title_rect, border_radius=5)
    pygame.draw.rect(surface, MILITARY_ACCENT,
                     title_rect, width=1, border_radius=5)

    # Title text
    title_surface = status_font.render(title, True, MILITARY_ACCENT)
    title_text_rect = title_surface.get_rect(
        center=(rect.x + rect.width//2, rect.y + 15))
    surface.blit(title_surface, title_text_rect)


def draw_spec_line(surface, x, y, label, value, color=MILITARY_TEXT, value_x_offset=150):
    label_surface = spec_font.render(f"{label}: ", True, MILITARY_ACCENT)
    surface.blit(label_surface, (x, y))
    value_surface = spec_font.render(str(value), True, color)
    surface.blit(value_surface, (x + value_x_offset, y))


def get_threat_color(threat_level):
    """Get color based on threat level."""
    if threat_level == "LOW":
        return MILITARY_ACCENT
    elif threat_level == "MEDIUM":
        return MILITARY_WARNING
    else:
        return (255, 0, 0)


def get_prediction(frame):
    image = cv2.resize(frame, (224, 224))
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    prediction = model.predict(image, verbose=0)
    index = np.argmax(prediction)
    return index, class_names[index], prediction[0][index], prediction[0]


def draw_wrapped_text(surface, text, x, y, font, color, max_width=400):
    import textwrap
    lines = textwrap.wrap(text, width=45)
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y + i * 18))


# Animation variables
last_detection = None
detection_change_time = 0

# Main loop
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        print("Webcam not available.")
        break

    frame = cv2.flip(frame, 1)
    prediction_index, class_name, confidence, all_confidences = get_prediction(
        frame)

    # Convert OpenCV to pygame surface
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
    frame_surface = pygame.transform.scale(frame_surface, (500, 400))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if detection changed
    if last_detection != class_name:
        last_detection = class_name
        detection_change_time = time.time()

    # Draw military background
    draw_military_background(screen)

    # Title
    title_surface = title_font.render(
        "TACTICAL AI RECONNAISSANCE SYSTEM", True, MILITARY_ACCENT)
    title_rect = title_surface.get_rect(center=(window_size[0]//2, 30))
    screen.blit(title_surface, title_rect)

    # Left side - Camera feed
    camera_panel = pygame.Rect(20, 80, 520, 480)
    draw_military_panel(screen, camera_panel, "LIVE FEED")

    # Camera feed
    screen.blit(frame_surface, (30, 120))

    # Camera border
    camera_border = pygame.Rect(28, 118, 504, 404)
    pygame.draw.rect(screen, MILITARY_ACCENT, camera_border, width=2)

    # Right side - Detection panel
    detection_panel = pygame.Rect(560, 80, 620, 480)
    draw_military_panel(screen, detection_panel, "TARGET ANALYSIS")

    # Main detection display
    detection_y = 130
    detected_surface = main_font.render(
        class_name.upper(), True, MILITARY_ACCENT)
    detected_rect = detected_surface.get_rect(center=(870, detection_y))
    screen.blit(detected_surface, detected_rect)

    # Confidence bar
    bar_width = 400
    bar_height = 20
    bar_x = 580
    bar_y = detection_y + 50
    bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(screen, MILITARY_DARK, bar_rect, border_radius=10)
    pygame.draw.rect(screen, MILITARY_ACCENT, bar_rect,
                     width=2, border_radius=10)

    # Fill bar based on confidence
    fill_width = int(bar_width * confidence)
    fill_rect = pygame.Rect(bar_x + 2, bar_y + 2,
                            fill_width - 4, bar_height - 4)
    pygame.draw.rect(screen, MILITARY_ACCENT, fill_rect, border_radius=8)

    # Confidence text
    conf_text = f"CONFIDENCE: {confidence * 100:.1f}%"
    conf_surface = sub_font.render(conf_text, True, MILITARY_TEXT)
    conf_rect = conf_surface.get_rect(center=(870, bar_y + 40))
    screen.blit(conf_surface, conf_rect)

    # Specifications panel
    specs_panel = pygame.Rect(580, detection_y + 120, 580, 360)
    draw_military_panel(screen, specs_panel,
                        "TACTICAL SPECIFICATIONS", MILITARY_DARK)

    # Get specs for current class
    specs = class_specs.get(class_name.lower())
    if not specs:
        specs = {
            "threat_level": "N/A",
            "classification": "N/A",
            "tactical_value": "N/A",
            "recommendation": "N/A",
            "description": f"No detailed data for '{class_name}'. Object detected as '{class_name}'.",
            "dimensions": "N/A",
            "weight": "N/A",
            "material": "N/A",
            "detection_range": "N/A",
            "mobility": "N/A",
            "thermal_signature": "N/A",
            "radar_cross_section": "N/A",
            "threat_assessment": "N/A",
            "countermeasures": "N/A",
            "intel_value": "N/A",
            "operational_impact": "N/A"
        }

    # Draw specifications in organized layout
    spec_start_y = detection_y + 160
    left_col_x = 640
    line_height = 32
    value_x_offset = 160

    # Left column - Basic specs
    draw_spec_line(screen, left_col_x, spec_start_y, "THREAT LEVEL",
                   specs["threat_level"], get_threat_color(specs["threat_level"]), value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + line_height,
                   "CLASSIFICATION", specs["classification"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 2*line_height,
                   "TACTICAL VALUE", specs["tactical_value"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 3*line_height,
                   "RECOMMENDATION", specs["recommendation"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 4*line_height,
                   "DIMENSIONS", specs["dimensions"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 5*line_height,
                   "WEIGHT", specs["weight"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 6*line_height,
                   "MATERIAL", specs["material"], MILITARY_TEXT, value_x_offset)
    draw_spec_line(screen, left_col_x, spec_start_y + 7*line_height,
                   "DETECTION RANGE", specs["detection_range"], MILITARY_TEXT, value_x_offset)

    # Description (multi-line) at bottom
    draw_wrapped_text(
        screen,
        specs["description"],
        left_col_x,
        spec_start_y + 8 * line_height,
        spec_font,
        MILITARY_TEXT,
        500
    )

    # Status panel at bottom
    status_panel = pygame.Rect(20, 580, 1160, 200)
    draw_military_panel(screen, status_panel, "SYSTEM STATUS")

    # Status information
    status_y = 620
    status_x = 40

    # System status
    system_status = "OPERATIONAL" if confidence > 0.3 else "DEGRADED"
    status_color = MILITARY_ACCENT if confidence > 0.3 else MILITARY_WARNING
    draw_spec_line(screen, status_x, status_y, "SYSTEM STATUS",
                   system_status, status_color)

    # Detection status
    detection_status = "ACTIVE" if confidence > 0.5 else "SCANNING"
    draw_spec_line(screen, status_x, status_y + 30,
                   "DETECTION STATUS", detection_status)

    # Time stamp
    timestamp = time.strftime("%H:%M:%S")
    draw_spec_line(screen, status_x, status_y + 60, "TIMESTAMP", timestamp)

    # FPS counter
    fps = clock.get_fps()
    draw_spec_line(screen, status_x, status_y + 90,
                   "FRAME RATE", f"{fps:.0f} FPS")

    pygame.display.update()
    clock.tick(30)

# Cleanup
cap.release()
pygame.quit()
sys.exit()

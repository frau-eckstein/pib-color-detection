import depthai as dai
import numpy as np
import cv2

# Funktion zur Zeichnung der Augen
def draw_eyes(image, dominant_color):
    # Berechne die Position und Größe der Augen
    eye1_center = (200, 150)
    eye2_center = (300, 150)
    eye_radius_x = 40
    eye_radius_y = 25

    # Zeichne die Augen
    cv2.ellipse(image, eye1_center, (eye_radius_x, eye_radius_y), 0, 0, 360, dominant_color, -1)
    cv2.ellipse(image, eye2_center, (eye_radius_x, eye_radius_y), 0, 0, 360, dominant_color, -1)

# Erstelle eine Pipeline
pipeline = dai.Pipeline()

# Konfiguriere Kameraeinstellungen
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(1000, 600)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(False)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Erstelle Output Streams
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# Starte die Pipeline
with dai.Device(pipeline) as device:
    # Starte den Preview-Stream
    q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        # Warte auf ein neues Bild
        in_rgb = q_rgb.get()
        # Konvertiere Bild zu numpy array
        frame = in_rgb.getCvFrame()
        
        # Finde den vorherrschenden RGB-Wert im Bild
        dominant_color = np.mean(frame, axis=(0, 1))
        
        # Speichere RGB-Werte in jeweiliger Variable
        red = dominant_color[2]
        green = dominant_color[1]
        blue = dominant_color[0]
        
        # Erstelle ein schwarzes Bild
        iris_image = np.zeros_like(frame)

        # Zeichne die Augen
        draw_eyes(iris_image, (int(blue), int(green), int(red)))

        # Zeige das Bild mit den Augen an
        cv2.imshow("Abstrakte Augen", iris_image)

        # Warte auf das Schließen des Fensters
        if cv2.waitKey(1) == ord('q'):
            break

    # Beende die OpenCV-Anzeige
    cv2.destroyAllWindows()

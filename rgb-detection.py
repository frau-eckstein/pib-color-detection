import depthai as dai
import numpy as np
import cv2

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
        
        # Speichere RGB-Werte in jeweliger Variable
        red = dominant_color[2]
        green = dominant_color[1]
        blue = dominant_color[0]
        
        color_rectangle = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.rectangle(color_rectangle, (0, 0), (300, 300), (int(blue), int(green), int(red)), -1)
        cv2.imshow("Farbe", color_rectangle)

        # Zeige den vorherrschenden RGB-Wert im Bild an
        # cv2.putText(frame, f"RGB: {dominant_color}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #cv2.putText(frame, f"Red: {red}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #cv2.putText(frame, f"Green: {green}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #cv2.putText(frame, f"Blue: {blue}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        
        # Zeige das Bild mit markiertem RGB-Wert an
        #cv2.imshow("RGB Image", frame)

        # Warte auf das Schließen des Fensters
        if cv2.waitKey(1) == ord('q'):
            break

    # Beende die OpenCV-Anzeige
    cv2.destroyAllWindows()

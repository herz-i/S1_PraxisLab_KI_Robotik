from ultralytics import YOLO
import cv2

def get_object_centers(image, model_path="yolo11n.pt"):
    """Detect objects and return their center coordinates."""
    model = YOLO(model_path)
    results = model(image)
    objects = []


    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
            class_id = int(box.cls[0])    # Class ID
            label = model.names[class_id] # Object name

            # Compute center coordinates in image space
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            #objects.append((label, center_x, center_y)) #center coordinates
            objects.append((label, x1, x2, y1, y2)) # Bounding box coordinates

    annotated_img = results[0].plot()

    cv2.imshow("Annotated", annotated_img)
    cv2.waitKey(5000)
    # cv2.destroyAllWindows()

    #print(objects)

    return objects
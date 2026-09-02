import cv2
import depthai as dai
import numpy as np
import time

class LuxonisCamera:
    def __init__(self) -> None:
        self.pipeline = dai.Pipeline()
        self.cam = None
        self.depth = None
        self.image = None
        #self.coords = []


    def get_image(self):
        "Get frame from camera and return image."

        color = (255, 255, 255)

        # Start streaming
        self.cam = self.pipeline.create(dai.node.Camera).build()
        qRGB = self.cam.requestOutput((640,400)).createOutputQueue()

        # Define sources and outputs for depth data
        depth = self.pipeline.create(dai.node.Depth).build(dai.node.Depth.Algorithm.AUTO, None, (640, 400))
        spatialLocationCalculator = self.pipeline.create(dai.node.SpatialLocationCalculator)

        initial_left = dai.Point2f(0.4, 0.4)
        initial_right = dai.Point2f(0.6, 0.6)

        self.config = dai.SpatialLocationCalculatorConfigData()
        self.config.depthThresholds.lowerThreshold = 10
        self.config.depthThresholds.upperThreshold = 10000
        self.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.MEDIAN
        self.config.roi = dai.Rect(initial_left, initial_right)

        spatialLocationCalculator.inputConfig.setWaitForMessage(False)
        spatialLocationCalculator.initialConfig.addROI(self.config)

        self.xoutSpatialQueue = spatialLocationCalculator.out.createOutputQueue()
        self.outputDepthQueue = spatialLocationCalculator.passthroughDepth.createOutputQueue()

        depth.depth.link(spatialLocationCalculator.inputDepth)

        self.inputConfigQueue = spatialLocationCalculator.inputConfig.createInputQueue()
 
        self.pipeline.start()

        img_raw = qRGB.get()
        assert isinstance(img_raw, dai.ImgFrame)
        self.image = img_raw.getCvFrame()

        for i in range(5):
            spatialData = self.xoutSpatialQueue.get().getSpatialLocations()
            
            outputDepthIMage : dai.ImgFrame = self.outputDepthQueue.get()
                    
            frameDepth = outputDepthIMage.getFrame()
            print("Median depth value: ", np.median(frameDepth))
            
            depthFrameColor = dai.utility.colorizeDepthFrame(outputDepthIMage).getCvFrame()

            # Show the frame
            cv2.imshow("depth", depthFrameColor)

            key = cv2.waitKey(1)
            if key == ord('q'):
                self.pipeline.stop()

            #self.pipeline.stop()
            for depthData in spatialData:
                roi = depthData.config.roi
                roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
                xmin = int(roi.topLeft().x)
                ymin = int(roi.topLeft().y)
                xmax = int(roi.bottomRight().x)
                ymax = int(roi.bottomRight().y)

                depthMin = depthData.depthMin
                depthMax = depthData.depthMax

                fontType = cv2.FONT_HERSHEY_TRIPLEX
                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)
                cv2.putText(depthFrameColor, f"X: {int(depthData.spatialCoordinates.x)} mm", (xmin + 10, ymin + 20), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Y: {int(depthData.spatialCoordinates.y)} mm", (xmin + 10, ymin + 35), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Z: {int(depthData.spatialCoordinates.z)} mm", (xmin + 10, ymin + 50), fontType, 0.5, color)
            time.sleep(1)
        return self.image

    def get_world_coordinates(self, x1, x2, y1, y2):
        "Convert center point from pixels to real-world 3D coordinates in camera frame."

        color = (255, 255, 255)

        # Define points of rectangle
        top_left = dai.Point2f(x1+50, y1)
        bottom_right = dai.Point2f(x2+50, y2)

        self.config.roi = dai.Rect(top_left, bottom_right)
        #self.config.calculationAlgorithm = calculationAlgorithm
        cfg = dai.SpatialLocationCalculatorConfig()
        cfg.addROI(self.config)
        self.inputConfigQueue.send(cfg)

        #self.pipeline.start()
        for i in range(5):
            spatialData = self.xoutSpatialQueue.get().getSpatialLocations()

            outputDepthIMage : dai.ImgFrame = self.outputDepthQueue.get()
            
            frameDepth = outputDepthIMage.getFrame()
            print("Median depth value: ", np.median(frameDepth))

            depthFrameColor = dai.utility.colorizeDepthFrame(outputDepthIMage).getCvFrame()

            coords = []

            for depthData in spatialData:
                roi = depthData.config.roi
                roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
                xmin = int(roi.topLeft().x)
                ymin = int(roi.topLeft().y)
                xmax = int(roi.bottomRight().x)
                ymax = int(roi.bottomRight().y)

                depthMin = depthData.depthMin
                depthMax = depthData.depthMax

                fontType = cv2.FONT_HERSHEY_TRIPLEX
                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)
                cv2.putText(depthFrameColor, f"X: {int(depthData.spatialCoordinates.x)} mm", (xmin + 10, ymin + 20), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Y: {int(depthData.spatialCoordinates.y)} mm", (xmin + 10, ymin + 35), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Z: {int(depthData.spatialCoordinates.z)} mm", (xmin + 10, ymin + 50), fontType, 0.5, color)

            time.sleep(1)
        coords.append((int(depthData.spatialCoordinates.x), int(depthData.spatialCoordinates.y), int(depthData.spatialCoordinates.z)))

        #cv2.rectangle(depthFrameColor, (278, 182), (315, 280), color, 2)
        #cv2.rectangle(depthFrameColor, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)



        return coords        


    def end_pipeline(self):
        self.pipeline.stop()
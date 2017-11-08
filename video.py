import pyyolo
import numpy as np
import sys
import cv2

darknet_path = 'pyyolo/darknet'
datacfg = 'cfg/coco.data'
cfgfile = 'cfg/tiny-yolo.cfg'
weightfile = '../tiny-yolo.weights'

thresh = 0.24
hier_thresh = 0.5

cam = cv2.VideoCapture(-1)

pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

step = 0
outputs = []

while 1:
	step+=1
	ret, image = cam.read()

	if step % 2 == 0:
		if not ret:
			print("Cannot connect to camera")
			pass

		img = image.transpose(2,0,1)
		c, h, w = img.shape[0], img.shape[1], img.shape[2]

		data = img.ravel()/255.0
		data = np.ascontiguousarray(data, dtype=np.float32)
		outputs = pyyolo.detect(w, h, c, data, thresh, hier_thresh)


	for output in outputs:
		cv2.putText(image, output['class'],(output['left'], output['top']), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,255),2)
		cv2.rectangle(image,(output['left'], output['top']), (output['right'], output['bottom']),(0,255,0),3)
		x = (output['left'] + output['right']) /2
		y = (output['top'] + output['bottom']) /2
		cv2.circle(image,(x, y), 4, (0,255,0), -1)

	cv2.imshow("Video",image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
# free model
pyyolo.cleanup()

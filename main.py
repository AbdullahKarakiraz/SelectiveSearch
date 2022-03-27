import argparse
import random
import time
import cv2

parser = argparse.ArgumentParser()

parser.add_argument("-i","--image",required=True,help = "path to input image")
parser.add_argument("-m","--method",type=str,default="fast",choices=["fast","quality"],help = "selective search methods")

args = vars(parser.parse_args())

image = cv2.imread(args["image"])

selective_search = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

selective_search.setBaseImage(image)

if args["method"] == "fast":
    selective_search.switchToSelectiveSearchFast()

else:
    selective_search.switchToSelectiveSearchQuality()
    
start_t = time.time()
process = selective_search.process()
stop_t = time.time()

print("search time : {:.2f}".format(stop_t - start_t))
print("total regions proposals : {}".format(len(process)))

for i in range(0,len(process),100):
    
    img_copy = image.copy()
    
    for (x,y,w,h) in process[i:i+100]:
        
        color = [random.randint(0, 255) for j in range(0, 3)]
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)
        
    cv2.imshow("image",img_copy)
    key = cv2.waitKey(0) & 0xff
    
    if key == ord("q"):
        break
    

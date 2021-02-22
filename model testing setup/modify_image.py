import cv2 as cv2


HSV_LIGHT_GREEN = (30,100, 80)
HSV_DARK_GREEN = (105,255,255)
IP_CAM_URL = 'http://192.168.50.194/live'

def get_modified_images(path):
    masked = create_green_mask(cv2.imread(path))
    cv2.imwrite(path.split('/')[0] + '/masked/' + path.split('/')[1], masked)
    edges = edge_detection(masked)
    cv2.imwrite(path.split('/')[0] + '/cannied/' + path.split('/')[1], edges)

def edge_detection(img):
    return cv2.Canny(img,100,200)

# Maskingfunction
def create_green_mask(img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, HSV_LIGHT_GREEN, HSV_DARK_GREEN)
    return cv2.bitwise_and(img, img, mask=mask)

def capture_image(path):
    ip_video = cv2.VideoCapture(IP_CAM_URL)
    ret, frame = ip_video.read()
    cv2.imwrite(path, frame)
    ip_video.release()

if __name__ == "__main__":
    filename = 'bf.jpg'
    image_path = "basil_fresh_1/"
    for index in range(15):
        input("Press Enter to capture frame...") 
        full_path = f'{image_path}{index}_{filename}'
        capture_image(full_path)
        get_modified_images(full_path)
        print('Image written to: ' + full_path)

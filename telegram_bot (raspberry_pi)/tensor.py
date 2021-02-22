import numpy as np
import tensorflow as tf

TFLITE_MODEL = '/home/pi/mediaprocessing/model/b1_masked_all_images_40epochs.tflite'
IMAGE_PATH =  '/home/pi/mediaprocessing/images/test/petersilie_umasked.jpg'
LABELS = [('basil', 'fresh'), ('basil', 'dry'), ('parsley', 'fresh'), ('parsley', 'dry')]


def get_label_of_image(image_path = IMAGE_PATH):
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load Image
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(240, 240))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image /= 255
    # Set and Invoke
    interpreter.set_tensor(input_details[0]['index'], [image])

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return LABELS[np.argmax(output_data)]
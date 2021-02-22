#!/Users/kian/.pyenv/versions/3.8.5/bin/python
import numpy as np
from numpy.lib.function_base import average
import tensorflow as tf
import os
from prettytable import PrettyTable as pt

# Load Image
def load_image(path):
    image = tf.keras.preprocessing.image.load_img(path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image /= 255
    return np.expand_dims(image, axis=0)

# Iterate over the models
def run_all(model_path, images):
    table = pt(['Model', 'Label', 'Hits', 'Misses', 'Average Certainty'])
    table.align = 'l'
    for file in sorted([file for file in os.listdir(model_path) if not file == 'info']):
        model = tf.keras.models.load_model(f'{model_path}/{file}')
        hits = 0
        misses = 0
        certainties = []
        current_label = images[0].split('/')[0] # get the label by path
        for image in images:
            prediction = model(load_image(image))
            certainties.append(np.max(prediction))
            if LABELS[np.argmax(prediction)] == current_label:
                hits += 1
            else:
                misses += 1
            if image.split('/')[0] != current_label:
                table.add_row([file, current_label, hits, misses, sum(certainties) / len(certainties)])
                print([file, current_label, hits, misses, sum(certainties) / len(certainties)])
                hits = 0
                misses = 0
                certainties = []
                current_label = image.split('/')[0]
        table.add_row([file, current_label, hits, misses, sum(certainties) / len(certainties)])
        print([file, current_label, hits, misses, sum(certainties) / len(certainties)])

    print_file(table)
    print(table)
    print_file(table.get_html_string())

def print_file(str):
    with open(f'{MODEL}_{MODE}.log', 'a') as file:
        print(str, file=file)

if __name__ == "__main__":
    LABELS = ['basil_fresh', 'basil_dry','parsley_fresh' , 'parsley_dry']
    MODEL = 'CUSTOM'
    MODE = 'cannied'
    MODEL_PATH = f'{MODEL}/{MODE}'
    IMAGE_SIZE = 240 if MODEL == 'B1' else 300
    IMAGES = []
    for label in LABELS:
        for file in os.listdir(f'{label}/{MODE}'):
            IMAGES.append(f'{label}/{MODE}/{file}')
    print_file(f'------------------- MODEL TESTING FOR {MODEL} MODE {MODE} --------------------')
    run_all(MODEL_PATH, IMAGES)

    
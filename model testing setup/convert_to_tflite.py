import tensorflow as tf


for i in range(1,11):
  path = f'results/k{i}.h5'
  converter = tf.lite.TFLiteConverter.from_keras_model(tf.keras.models.load_model(path))
  tflite_model = converter.convert()
  # Save the model.
  with open(f'k{i}.tflite', 'wb') as f:
    f.write(tflite_model)
    print(f'tflite Model written to: k{i}.tflite')
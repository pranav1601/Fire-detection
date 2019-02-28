from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True




train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    shear_range=0.2,
                    zoom_range=0.2,
                    horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
            
training_set = train_datagen.flow_from_directory(
                    'dataset/training_dataset',
                    target_size=(320, 240),
                    batch_size=32,
                    class_mode='binary')
            
test_set = test_datagen.flow_from_directory(
                    'dataset/test_dataset',
                    target_size=(320, 240),
                    batch_size=512,
                    class_mode='binary')

#dense_layers = [0,1,2]
#layer_sizes = [32,64,128]
#conv_layers = [1,2,3]
dense_layers = [2]
layer_sizes = [64]
conv_layers = [3]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
#            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
#            print(NAME)
            

            classifier = Sequential()

            classifier.add(Convolution2D(32,3,3,input_shape=(320,240,3),activation='relu'))
            
            classifier.add(MaxPooling2D(pool_size=(2, 2)))

            for l in range(conv_layer-1):
                classifier.add(Convolution2D(32,3,3,activation='relu'))
                classifier.add(MaxPooling2D(pool_size=(2, 2)))

            classifier.add(Flatten())
            for _ in range(dense_layer):
                classifier.add(Dense(layer_size),activation='relu')
                
                

            classifier.add(Dense(units=1,activation='sigmoid'))
            
            

            classifier.compile(optimizer='adam',metrics=['accuracy'],loss='binary_crossentropy')
            
            classifier.fit_generator(
                    training_set,
                    steps_per_epoch=62,
                    epochs=10,
                    validation_data=test_set,
                    validation_steps=5)





classifier.save('ip.h5')






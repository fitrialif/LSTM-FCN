from keras.models import Model
from keras.layers import Input, PReLU, Dense,Dropout, LSTM, Bidirectional, multiply, concatenate
from keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Activation

from utils.constants import MAX_SEQUENCE_LENGTH_LIST, NB_CLASSES_LIST
from utils.keras_utils import train_model, evaluate_model, set_trainable, visualize_cam

DATASET_INDEX = 9
OUTPUT_DIM = 1000

MAX_SEQUENCE_LENGTH = MAX_SEQUENCE_LENGTH_LIST[DATASET_INDEX]

NB_CLASS = NB_CLASSES_LIST[DATASET_INDEX]

TRAINABLE = True

def generate_model():
    ip = Input(shape=(1, MAX_SEQUENCE_LENGTH))

    x = LSTM(64)(ip)
    x = Dropout(0.8)(x)

    y = Permute((2, 1))(ip)
    y = Conv1D(128, 8, padding='same', kernel_initializer='he_uniform')(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)

    y = Conv1D(256, 5, padding='same', kernel_initializer='he_uniform')(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)

    y = Conv1D(128, 3, padding='same', kernel_initializer='he_uniform')(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)

    y = GlobalAveragePooling1D()(y)

    x = concatenate([x, y])

    out = Dense(NB_CLASS, activation='softmax')(x)

    model = Model(ip, out)

    cnn_count = 0
    for layer in model.layers:
        if layer.__class__.__name__ in ['Conv1D',
                                        'BatchNormalization',
                                        'PReLU']:
            if layer.__class__.__name__ == 'Conv1D':
                cnn_count += 1

            if cnn_count == 3:
                break
            else:
                set_trainable(layer, TRAINABLE)

    model.summary()

    #model.load_weights("weights/phalanx_age_group_weights - 7984.h5")

    return model


if __name__ == "__main__":
    model = generate_model()

    train_model(model, DATASET_INDEX, dataset_prefix='phalanx_age_group', epochs=2000, batch_size=128)

    evaluate_model(model, DATASET_INDEX, dataset_prefix='phalanx_age_group', batch_size=128)

    #visualize_cam(model, DATASET_INDEX, dataset_prefix='phalanx_age_group', class_id=0)

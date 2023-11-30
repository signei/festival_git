#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from keras.models import load_model
import pandas as pd
import random as rn
import os

import librosa

import librosa.display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# from keras.models import Sequential

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# import keras
# from keras.callbacks import ReduceLROnPlateau
# from keras.models import Sequential
# from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization
# from keras.utils import np_utils, to_categorical
# from keras.callbacks import ModelCheckpoint

# import tensorflow as tf
# from tensorflow.keras.models import Sequential, Model
# from tensorflow.keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D, Conv2D, MaxPool2D, ZeroPadding2D, BatchNormalization, Input, DepthwiseConv2D, Add, LeakyReLU, ReLU
# from tensorflow.keras.optimizers import Adam, SGD

# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import glob
import numpy as np
import pandas as pd
import parselmouth
import statistics

from parselmouth.praat import call
from scipy.stats.mstats import zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
import joblib
import pickle


def get_numpy_from_nonfixed_2d_array(aa, fixed_length, padding_value=0):
    rows = []
    for a in aa:
        rows.append(np.pad(a, (0, fixed_length), 'constant',
                    constant_values=padding_value)[:fixed_length])
    return np.concatenate(rows, axis=0).reshape(-1, fixed_length)


def all_seed(seed_num):
    np.random.seed(seed_num)
    rn.seed(seed_num)
    os.environ['PYTHONHASHSEED'] = str(seed_num)
    # tf.random.set_seed(seed_num)


seed_num = 42
all_seed(seed_num)


def get_feature(path):

    sample, sample_rate = librosa.load(path)
    # result = set_length(sample, maxlen)

    result = np.array([])

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(
        y=sample, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel))

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=sample, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc))

    return result


class Features:

    def measurePitch(voiceID, f0min, f0max, unit):
        sound = parselmouth.Sound(voiceID)  # read the sound
        duration = call(sound, "Get total duration")  # duration
        # create a praat pitch object
        pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
        meanF0 = call(pitch, "Get mean", 0, 0, unit)  # get mean pitch
        stdevF0 = call(pitch, "Get standard deviation", 0,
                       0, unit)  # get standard deviation
        harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
        hnr = call(harmonicity, "Get mean", 0, 0)
        pointProcess = call(
            sound, "To PointProcess (periodic, cc)", f0min, f0max)
        localJitter = call(pointProcess, "Get jitter (local)",
                           0, 0, 0.0001, 0.02, 1.3)
        localabsoluteJitter = call(
            pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        rapJitter = call(pointProcess, "Get jitter (rap)",
                         0, 0, 0.0001, 0.02, 1.3)
        ppq5Jitter = call(pointProcess, "Get jitter (ppq5)",
                          0, 0, 0.0001, 0.02, 1.3)
        ddpJitter = call(pointProcess, "Get jitter (ddp)",
                         0, 0, 0.0001, 0.02, 1.3)
        localShimmer = call([sound, pointProcess],
                            "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        localdbShimmer = call(
            [sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq3Shimmer = call([sound, pointProcess],
                           "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        aqpq5Shimmer = call([sound, pointProcess],
                            "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq11Shimmer = call([sound, pointProcess],
                            "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        ddaShimmer = call([sound, pointProcess],
                          "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

        return duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer

    def measureFormants(sound, wave_file, f0min, f0max):
        sound = parselmouth.Sound(sound)  # read the sound
        pitch = call(sound, "To Pitch (cc)", 0, f0min, 15,
                     'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
        pointProcess = call(
            sound, "To PointProcess (periodic, cc)", f0min, f0max)

        formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
        numPoints = call(pointProcess, "Get number of points")

        f1_list = []
        f2_list = []
        f3_list = []
        f4_list = []

        # Measure formants only at glottal pulses
        for point in range(0, numPoints):
            point += 1
            t = call(pointProcess, "Get time from index", point)
            f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
            f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
            f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
            f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
            f1_list.append(f1)
            f2_list.append(f2)
            f3_list.append(f3)
            f4_list.append(f4)

        f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
        f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
        f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
        f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']

        # calculate mean formants across pulses
        f1_mean = np.nanmean(np.array(f1_list))
        f2_mean = np.nanmean(np.array(f2_list))
        f3_mean = np.nanmean(np.array(f3_list))
        f4_mean = np.nanmean(np.array(f4_list))

        # calculate median formants across pulses, this is what is used in all subsequent calcualtions
        # you can use mean if you want, just edit the code in the boxes below to replace median with mean
        f1_median = np.nanmedian(np.array(f1_list))
        f2_median = np.nanmedian(np.array(f2_list))
        f3_median = np.nanmedian(np.array(f3_list))
        f4_median = np.nanmedian(np.array(f4_list))

        return f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median

    def runPCA(df):
        # z-score the Jitter and Shimmer measurements
        measures = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                    'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
        # x = df.loc[:, measures].values
        x = df.loc[:, measures].apply(pd.to_numeric, errors='coerce').values
        if np.isnan(x).any() or np.isinf(x).any():
            # Replace all NaNs with 0 and all infinities with large finite numbers
            x = np.nan_to_num(x)
        x = StandardScaler().fit_transform(x)
        # PCA
        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(x)
        principalDf = pd.DataFrame(data=principalComponents, columns=[
                                   'JitterPCA', 'ShimmerPCA'])
        principalDf
        return principalDf

    def formantext(audio):
        file_list = []
        duration_list = []
        mean_F0_list = []
        sd_F0_list = []
        hnr_list = []
        localJitter_list = []
        localabsoluteJitter_list = []
        rapJitter_list = []
        ppq5Jitter_list = []
        ddpJitter_list = []
        localShimmer_list = []
        localdbShimmer_list = []
        apq3Shimmer_list = []
        aqpq5Shimmer_list = []
        apq11Shimmer_list = []
        ddaShimmer_list = []
        f1_mean_list = []
        f2_mean_list = []
        f3_mean_list = []
        f4_mean_list = []
        f1_median_list = []
        f2_median_list = []
        f3_median_list = []
        f4_median_list = []

        # Go through all the wave files in the folder and measure all the acoustics
        for wave_file in glob.glob(audio + "*.wav"):
            sound = parselmouth.Sound(wave_file)
            (duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter,
             localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = Features.measurePitch(
                sound, 75, 300, "Hertz")
            (f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median) = Features.measureFormants(
                sound, wave_file, 75, 300)
            file_list.append(wave_file)  # make an ID list
            duration_list.append(duration)  # make duration list
            mean_F0_list.append(meanF0)  # make a mean F0 list
            sd_F0_list.append(stdevF0)  # make a sd F0 list
            hnr_list.append(hnr)  # add HNR data

            # add raw jitter and shimmer measures
            localJitter_list.append(localJitter)
            localabsoluteJitter_list.append(localabsoluteJitter)
            rapJitter_list.append(rapJitter)
            ppq5Jitter_list.append(ppq5Jitter)
            ddpJitter_list.append(ddpJitter)
            localShimmer_list.append(localShimmer)
            localdbShimmer_list.append(localdbShimmer)
            apq3Shimmer_list.append(apq3Shimmer)
            aqpq5Shimmer_list.append(aqpq5Shimmer)
            apq11Shimmer_list.append(apq11Shimmer)
            ddaShimmer_list.append(ddaShimmer)

            # add the formant data
            f1_mean_list.append(f1_mean)
            f2_mean_list.append(f2_mean)
            f3_mean_list.append(f3_mean)
            f4_mean_list.append(f4_mean)
            f1_median_list.append(f1_median)
            f2_median_list.append(f2_median)
            f3_median_list.append(f3_median)
            f4_median_list.append(f4_median)

        df = pd.DataFrame(np.column_stack([file_list, duration_list, mean_F0_list, sd_F0_list, hnr_list,
                                           localJitter_list, localabsoluteJitter_list, rapJitter_list,
                                           ppq5Jitter_list, ddpJitter_list, localShimmer_list,
                                           localdbShimmer_list, apq3Shimmer_list, aqpq5Shimmer_list,
                                           apq11Shimmer_list, ddaShimmer_list, f1_mean_list,
                                           f2_mean_list, f3_mean_list, f4_mean_list,
                                           f1_median_list, f2_median_list, f3_median_list,
                                           f4_median_list]),
                          columns=['voiceID', 'duration', 'meanF0Hz', 'stdevF0Hz', 'HNR',
                                   'localJitter', 'localabsoluteJitter', 'rapJitter',
                                   'ppq5Jitter', 'ddpJitter', 'localShimmer',
                                   'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                                   'apq11Shimmer', 'ddaShimmer', 'f1_mean', 'f2_mean',
                                   'f3_mean', 'f4_mean', 'f1_median',
                                   'f2_median', 'f3_median', 'f4_median'])

        pcaData = Features.runPCA(df)  # Run jitter and shimmer PCA
        df = pd.concat([df, pcaData], axis=1)  # Add PCA data

        df['f1_median'] = pd.to_numeric(df['f1_median'], errors='coerce')
        df['f2_median'] = pd.to_numeric(df['f2_median'], errors='coerce')
        df['f3_median'] = pd.to_numeric(df['f3_median'], errors='coerce')
        df['f4_median'] = pd.to_numeric(df['f4_median'], errors='coerce')

        df['pF'] = (zscore(df['f1_median']) + zscore(df['f2_median']) +
                    zscore(df['f3_median']) + zscore(df['f4_median'])) / 4

        df['fdisp'] = (df['f4_median'] - df['f1_median']) / 3

        df['avgFormant'] = (df['f1_median'] + df['f2_median'] +
                            df['f3_median'] + df['f4_median']) / 4

        df['mff'] = (df['f1_median'] * df['f2_median'] *
                     df['f3_median'] * df['f4_median']) ** 0.25

        df['fitch_vtl'] = ((1 * (35000 / (4 * df['f1_median']))) +
                           (3 * (35000 / (4 * df['f2_median']))) +
                           (5 * (35000 / (4 * df['f3_median']))) +
                           (7 * (35000 / (4 * df['f4_median'])))) / 4

        xysum = (0.5 * df['f1_median']) + (1.5 * df['f2_median']) + \
            (2.5 * df['f3_median']) + (3.5 * df['f4_median'])
        xsquaredsum = (0.5 ** 2) + (1.5 ** 2) + (2.5 ** 2) + (3.5 ** 2)
        df['delta_f'] = xysum / xsquaredsum

        df['vtl_delta_f'] = 35000 / (2 * df['delta_f'])

        newdf = df.drop(df.columns[[1]], axis=1)

        # print("finished")
        # print(newdf.iloc[:,1:])
        # print(newdf.shape)

        return newdf.iloc[:, 1:]


def inference(name, path):
    x = []

    for file in os.listdir(path):
        if 'wav' in file:
            file_name = file
            audio = get_feature(os.path.join(path, file_name))
            audio = np.array(audio)
            x.append(audio)

    formant1 = Features.formantext(path)
    formant1_pre = formant1.to_numpy()

    x = np.array(x)
    x = np.hstack((x, formant1_pre))

    path = 'C:/Users/bio/Documents/festival/'

    if name == 'criminal1':
        with open('rf_criminal1.pkl', 'rb') as f: 
            rf_from_joblib = pickle.load(f)
        print("criminal1")
    elif name == 'criminal2':
        with open('rf_criminal2.pkl', 'rb') as f: 
            rf_from_joblib = pickle.load(f)
        print("criminal2")
    elif name == 'glory':
        with open('rf_glory.pkl', 'rb') as f: 
            rf_from_joblib = pickle.load(f)
        print("glory")
    elif name == 'gambler':
        with open('rf_gambler.pkl', 'rb') as f: 
            rf_from_joblib = pickle.load(f)
        print("gambler")

    pred = rf_from_joblib.predict_proba(x)

    # mean = round((pred[0][1] + pred[1][1]) / 2 * 100, 2)
    maxval_1 = round((pred[0][1]) * 100, 2)
    maxval_2 = round((pred[1][1]) * 100, 2)
    if maxval_1 > maxval_2:
        return maxval_1
    elif maxval_1 < maxval_2:
        return maxval_2

    # return mean

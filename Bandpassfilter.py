import librosa
import os
import scipy.signal
import matplotlib.pyplot as plt
import csv
import numpy as np

SAMPLE_RATE = 4000

def ButterBandpass(low, high, fs, order=3):
    sos = scipy.signal.butter(order, [low, high], btype='bandpass', fs=fs, output='sos')

    return sos

def ApplyBandpass(filePath, low, high, order=3):
    numArray, sampleRate = librosa.load(filePath, sr=None)
    sos = ButterBandpass(low, high, sampleRate, order)
    filtered = scipy.signal.sosfiltfilt(sos, numArray)

    return filtered

def SegmentArray(digitalStream, segmentPath):
    segmenterOutput = [] 
    windows = []
    seg = startTime = None
    with open(segmentPath, encoding= "utf-8") as fh:
        for line in fh:
            row = line.split("\t")
            label = int(row[-1].strip())
            if label == 1:
                seg = 1
                startTime = float(row[0].strip())
            elif seg is not None and label == seg + 1:
                seg += 1
                if seg == 4:
                    endTime =  float(row[1].strip())
                    windows.append((startTime, endTime))
            else:
                seg = startTime = None
            
    for cycle in windows:
        startIndex, endIndex = int(cycle[0]*SAMPLE_RATE), int(cycle[1]*SAMPLE_RATE)
        segmenterOutput.append(digitalStream[startIndex: endIndex + 1])

    return segmenterOutput


if __name__ == "__main__":
    with open("manifest.csv") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            tsvFile = row["seg_filepath"]
            audioPath = row["filepath"]
            audioPath = os.path.expanduser(f"~/the-circor-digiscope-phonocardiogram-dataset-1.0.3/{audioPath}")
            segmentPath = os.path.expanduser(f"~/the-circor-digiscope-phonocardiogram-dataset-1.0.3/{tsvFile}")
            filteredAudio = ApplyBandpass(audioPath, 25, 400)
            segmentedAudio = SegmentArray(filteredAudio, segmentPath)
            print(segmentedAudio)

        



"""
from this:

patient_id,recording_locations,age,sex,height,weight,pregnancy_status,murmur
2530,AV+PV+TV+MV,Child,Female,98.0,15.9,False,Absent
9979,AV+PV+TV+MV,Child,Female,103.0,13.1,False,Present
13918,AV+PV+TV+MV,Child,Male,98.0,15.9,False,Present
14241,AV+PV+TV+MV,Child,Male,87.0,11.2,False,Present
23625,AV+PV+TV+MV,Child,Female,92.0,14.0,False,Absent

We want something like this:

filepath, patient_id, location, age, sex, label
training_data/2530_AV.wav, 2530, AV, Child, Female, Absent
training_data/2530_PV.wav, 2530, PV, Child, Female, Absent
training_data/2530_TV.wav, 2530, TV, Child, Female, Absent

in our manifest.
"""

import os
from csv import DictReader, DictWriter
def generate(filepath, delimeter=","):
    noOfGeneratedPathss = 0
    noOfSkippedPaths = 0
    fileDict = dict()
    with open(filepath) as fh:
        fileDict = DictReader(fh, delimiter=delimeter)
        csv = []
        rowdict = {}
        for row in fileDict:
            locations = row["recording_locations"].strip().split("+")
            for location in locations:
                rowdict["filepath"] = f"training_data/{row["patient_id"].strip()}_{location}.wav"
                rowdict["age"] = row["age"].strip()
                rowdict["location"] = location.strip()
                rowdict["sex"] = row["sex"].strip()
                rowdict["patient_id"] = row["patient_id"].strip()
                rowdict["murmur"] = row["murmur"].strip()
                audioPath = os.path.expanduser(f"~/the-circor-digiscope-phonocardiogram-dataset-1.0.3/{rowdict["filepath"]}")
                segFile = rowdict["filepath"][:len(rowdict["filepath"]) - 3] + "tsv"
                segmentPath = os.path.expanduser(f"~/the-circor-digiscope-phonocardiogram-dataset-1.0.3/{segFile}")
                if os.path.exists(audioPath) and os.path.exists(segmentPath):
                    rowdict["seg_filepath"] = f"training_data/{row['patient_id'].strip()}_{location}.tsv"
                    csv.append(rowdict)
                    noOfGeneratedPathss += 1
                    rowdict = {}
                else:
                    noOfSkippedPaths += 1
    
    headers = csv[0].keys() 
    with open("manifest.csv", 'w', newline="") as outputFh:
        writerDict = DictWriter(outputFh, fieldnames=headers)
        # write header row
        writerDict.writeheader()
        # write all data
        writerDict.writerows(csv)
    print(f"Generated {noOfGeneratedPathss} and skipped {noOfSkippedPaths}")
    print("succesful")

if __name__ == "__main__":
    generate("./clean_data.csv")
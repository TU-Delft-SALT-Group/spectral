from fastapi import HTTPException

from .signal_analysis import simple_signal_info
from .frame_analysis import (
    simple_frame_info,
    calculate_frame_f1_f2
)

def simple_info_mode(data,fs,file,frame_index):
    result = simple_signal_info(data,fs)
    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]
    result["frame"] = simple_frame_info(data,fs,frame_index)
    return result
    
def spectogram_mode(data,fs,frame_index):
    result = "hi"
    return result

def vowel_space_mode(data,fs,frame_index):
    if frame_index is None:
        raise HTTPException(
            status_code=400, detail="Vowel-space mode was not given frame"
        )
    frame_data = data[frame_index["startIndex"]:frame_index["endIndex"]]
    formants = calculate_frame_f1_f2(frame_data,fs)
    return {"f1":formants[0],"f2":formants[1]}
    
    
    
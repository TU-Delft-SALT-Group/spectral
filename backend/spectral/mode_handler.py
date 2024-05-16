from .signal_analysis import simple_signal_info
from .frame_analysis import simple_frame_info

def simple_info_mode(data,fs,file,frame_index):
    result = simple_signal_info(data,fs)
    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]
    result["frame"] = simple_frame_info(data,fs,frame_index)
    return result
    
    
def spectogram_mode(data,fs,frame_index):
    result = "hi"
    return result
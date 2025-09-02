from typing import Tuple
import pandas as pd

def process_labels(data) -> Tuple[pd.Series, pd.DataFrame]:
    """
    This is a recreation of work I did to help process different label types on a ML model. For this example suppose we have a pandas dataframe that we are using for training,
    but there are three labels that come packaged in this data. we have determined that we will prioritize the types of labels as Manual Label <- Camera Label <- Sensor Label.
    We will also suppose that we want to remove sub-labels of lower priority when they do not coincide with a higher priority label, and since the environment I was working in was
    python 3.9 we will also suppose match case is not usable.

    ****Please note that this may not makes sense out of context since this example is using camera, and sensors as our "data" This is the best approximation for the actual data I 
    was working with.****

    This function will create a series of labels based on the highest priorty label, and we will create an attribute matrix the will allows us to remove sub-labels from the data
    in later functions so that we avoid the possibility of data poisoning.

    Arg:
    data (pd.DataFrame): This is the data we will eventually use to train our model.

    Return:
    labels (pd.Series): This is a Series of labels that will eventually be fed into our model.
    label_matrix (pd.DataFrame): This is a matrix that will be used by another function to identify which labels need to be removed.
    """

    # Based on analysis of the data we know there will always be a "sensor label" so we will copy that column as our starting point.
    labels = data["sensorLabel"].copy()

    # Overwrite indexes in the series when "cameraLabel" is not empty or not NA
    data["cameraLabel"].fillna(value="", inplace=True)
    data["cameraLabel"] = data["cameraLabel"].astype("string")
    camera_indices = data["cameraLabel"] != ""
    labels[camera_indices] = data["cameraLabel"][camera_indices]

    # Do the same thing with manual Label
    data["manualLabel"].fillna(value="", inplace=True)
    data["manualLabel"] = data["manualLabel"].astype("string")
    manual_indices = data["manualLabel"] != ""
    labels[manual_indices] = data["manualLabel"][manual_indices]

    # Create boolean comparisons that will be used to create our attribute matrix
    camera_sensor_match = data["sensorLabel"] == data["cameraLabel"]
    manual_sensor_match = data["sensorLabel"] == data["manualLabel"]
    manual_camera_match = data["cameraLabel"] == data["manualLabel"]

    # Combine needed fields into attribute matrix
    attribute_matrix = pd.concat([
        camera_indices.rename("cameraIndices"),
        manual_indices.rename("manualIndices"),
        camera_sensor_match.rename("cameraSensorMatch"),
        manual_sensor_match.rename("manualSensorMatch"),
        manual_camera_match.rename("manualCameraMatch")],
        axis=1
    )

    return labels, attribute_matrix

def create_attribute_update_conditions(attribute_matrix) -> Tuple [pd.Series, pd.Series, pd.Series]:
    """
    This function will act as our match case system. Since we have several conditions that could warrant the removal of labels we will take of Attribute matrix and perform a series
    of vector check to reduce them into 3 seperate boolean Series that will be passed to another function that will remove the labels within the data appropriately.
    This function will have a lot more comments than the code currently in production for ease of understanding the different conditions.

    Arg:
    attribute_matrix (pd.DataFrame): This will be our attribute matrix that will have all of our label matchs we will using to set label removal conditions

    Return:
    remove_sensor (pd.Series): A series of booleans that will tell another function to remove the sensor label
    remove_camera (pd.Series): A series of booleans that will tell another function to remove the camera label
    remove_both (pd.Series): A series of booleans that will tell another function to remove both the camera and sensor labels
    """
    # Create the rules that dictate removal of remove sensor sub label
    cond1 = attribute_matrix["manualIndices"] & ~attribute_matrix["manualSensorMatch"]
    cond2 = ~attribute_matrix["manualIndices"] & attribute_matrix["cameraIndices"] & ~attribute_matrix["cameraSensorMatch"]

def remove_sub_labels(data, remove_camera_label, remove_sensor_label, remove_both):
    if remove_both.any():
    	data.loc[remove_both, “cameraLabel”] = “”
    	data.loc[remove_both, “sensorLabel”] = “”
    if remove_camera_label.any():
    data.loc[remove_camera_label, “cameraLabel”]  = “”
    if remove_sensor_label.any():
    	data.loc[remove_sensor_label, “sensorLabel”] = “”
    return data

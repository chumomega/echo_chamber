#import labels from model.GeminiClient
from model.GeminiClient import POLITICAL_LABELS

#political labels manually listed out
#POLITICAL_LABELS = ["communist", "leftist", "liberal", "moderate", "conservative", "nationalist"]

def avg_of_objects(dicts_of_json: dict) -> dict:
#labels to dynamically create dictionary 
    labels = POLITICAL_LABELS
    sub_labels = ["total_magnitude", "avg_magnitude", "percent_of_whole"]
    default_value = 0
#Ceate dictionary to return
    weighted_avg = {
        label: {sub_label: default_value for sub_label in sub_labels} for label in labels
    }
#Total Magnitude of input tracked to determine percentage of whole for each label
    total_sum_of_magnitudes = 0
#This is necessary if the inputted dictionary will have a key as in the example output of the gemini client
    dict_to_search = dicts_of_json["example_output"]
#Update Weighted Average dictionary
#For each response...
    for response in dict_to_search:
#and for each label in this response
        for label in labels:
#Update total magnitude for label
            weighted_avg[label]["total_magnitude"]+=dict_to_search[response][label]
#Update total magnitudes for entire page
            total_sum_of_magnitudes+=dict_to_search[response][label]
#Length of Input
    total_responses=len(dict_to_search)
#Update Avg_Magnitude and Percent_of_Whole for each label only once. (as opposed to for each response in the loop above)
    for label in labels:
        weighted_avg[label]["avg_magnitude"]=weighted_avg[label]["total_magnitude"]/total_responses
        weighted_avg[label]["percent_of_whole"]=weighted_avg[label]["total_magnitude"]/total_sum_of_magnitudes

#Return Dictionary
    return weighted_avg
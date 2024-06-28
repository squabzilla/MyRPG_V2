import os
import pathlib

# takes my text files of features
# examines the text to figure out what values to add in the non-text columns
# turns it into a CSV with:
    # text_id - primary key
    # feature_id - id for all the text-boxes that belong to one feature
    # text_type - the display type of this element - title, subtitle, etc
    # text_order - the order that these text-boxes appear in for the feature
    # text_text - the actual text, which this script puts into quotations

input_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\RegexModded_TextFiles")
output_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\TextToCSVs")

var_file_names = ["aaa_class_features_lines", "BarbarianFeatures","BardFeatures","ClericFeatures",
                "DruidFeatures","FighterFeatures","MonkFeatures",
                "PaladinFeatures","RangerFeatures","RogueFeatures",
                "SorcererFeatures","WarlockFeatures","WizardFeatures"]
input_path_names = []
output_path_names = []
for i in range(len(var_file_names)):
    #var_file_names[i] = var_file_names[i] + ".txt"
    #var_RegexModdedText_paths.append(pathlib.Path.joinpath(var_output_RegexModdedText_path, var_RegexModdedText_names[i]))
    input_path_names.append(pathlib.Path.joinpath(input_path, (var_file_names[i] + ".txt")))
    output_path_names.append(pathlib.Path.joinpath(output_path, (var_file_names[i] + ".csv")))

def find_shortest(input_path_name):
    #test_file = input_path_names[0]
    var_file = input_path_name
    shortest = 2 * 1000 * 1000 * 1000
    with open(var_file, 'r', encoding='utf-8') as file:
        lines = [line.rstrip() for line in file] # <- store line-by-line in lines, but without line-break at end
        for line in lines:
            if len(line) < 6: print(line)
            if len(line) < shortest:
                shortest = len(line)
    return shortest

def main():
    for i in range(len(var_file_names)):
        shortest = find_shortest(input_path_names[i])
        #print(f"The shortest line-count in {var_file_names[i]} is: {shortest}")
        
main()
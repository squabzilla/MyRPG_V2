import os
import re
import pathlib
import shutil

### NOTE: Purpose:
# When I grabbed the text from the PDF, the width of text columns split up sentences and paragraphs onto new lines
# The goal of this text is to find all of the "artificial" new-lines, and remove them.
# However, change in style - such as from title to text - paragraph breaks, bullet-points, etcl. are to be preserved
# honestly I ended up going through it manually to mark all the paragraph breaks but whatever, this should still work
# NOTE: the SRD I'm working from does have tab-indentation visible to mark new paragraphs
# Therefore, even if a sentence ends in a period, if the start of the next line isn't tab, I want to remove the newline
# (to mark it as part of one paragraph)
# I manually added my own signifiers in the text, since the tab-indentation is only visually visible on the PDF -
# I'm sure they exist somewhere, but I don't know of a way to programatically read the PDF
# In fact, I ended up taking screen-shots and OCR'ing it. Really would've been looking for software that just reads 
# raw PDF data and let's me manipulate it, but that's not what I did.

# Full paths: (depreciated)
#var_inputText_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\TextFiles")
#var_output_RegexModdedText_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\TextFiles_RegexAltered")

# relative folder paths for input and output folders:
var_inputText_path = "static/CSVs/TextFiles"
var_output_RegexModdedText_path = "static/CSVs/TextFiles_RegexAltered"

# setting them up properly as path variables (with full path)
main_dir = os.path.dirname(os.getcwd())
var_inputText_path = os.path.join(main_dir, var_inputText_path)
var_inputText_path = pathlib.Path(var_inputText_path)
var_output_RegexModdedText_path = os.path.join(main_dir, var_output_RegexModdedText_path)
var_output_RegexModdedText_path = pathlib.Path(var_output_RegexModdedText_path)


var_file_names = ["aaa_class_features_lines", "BarbarianFeatures","BardFeatures","ClericFeatures",
                "DruidFeatures","FighterFeatures","MonkFeatures",
                "PaladinFeatures","RangerFeatures","RogueFeatures",
                "SorcererFeatures","WarlockFeatures","WizardFeatures"]

# Name variables
var_inputText_names = []
var_RegexModdedText_names = []

# path variables
# NOTE: I want these later
var_inputText_paths = []
var_RegexModdedText_paths = []

# extension variables
var_text_end = ".txt"
var_csv_end = ".csv"

# actual folder-paths
#var_inputText_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\TextFiles")
#var_output_RegexModdedText_path = pathlib.Path("D:\GitProjects\CS50-FinalProject\Main\static\CSVs\RegexModded_TextFiles")
#print(var_output_RegexModdedText_path)

# amount of files
var_number_of_files = len(var_file_names)

# let's set them up correct
for i in range(var_number_of_files):
    var_inputText_names.append(pathlib.Path(var_file_names[i] + var_text_end))
    var_RegexModdedText_names.append(pathlib.Path(var_file_names[i] + var_text_end))
    var_inputText_paths.append(pathlib.Path.joinpath(var_inputText_path, var_inputText_names[i]))
    var_RegexModdedText_paths.append(pathlib.Path.joinpath(var_output_RegexModdedText_path, var_RegexModdedText_names[i]))

# just some stuff I want in a list
var_integers = str(1234567890)
var_lowercase = "abcdefghijklmnopqrstuvwxyz"
var_uppercase = var_lowercase.upper()
var_other_chars = [","]
var_regex_escape_chars = ["+", "."] #some of these characters might be ones regex treats fucky
#var_other_chars = [",","\+","\."] 
#var_other_chars = [",", "+", "."]
#var_pound_sign = "\$" #regex also treats this fucky
var_all_chars = []

#filling up my list of chars I want:
for item in var_integers:
    var_all_chars.append(item)
for item in var_lowercase:
    var_all_chars.append(item)
for item in var_uppercase:
    var_all_chars.append(item)
for i in range(len(var_other_chars)):
    var_all_chars.append(var_other_chars[i])


# pieces I'm swapping out
var_find_end = "\\n"
var_replace_end = " "

# lists of find and replace
# NOTE: I want these later
var_list_find_items = []
var_list_replace_items = []

for var_char in var_all_chars:
    var_list_find_items.append(var_char + var_find_end)
    var_list_find_items.append(var_char + " " + var_find_end)
    var_list_replace_items.append(var_char + var_replace_end)
    var_list_replace_items.append(var_char + " " + var_replace_end)
for item in var_regex_escape_chars:
    var_list_find_items.append("\\" + item + var_find_end)
    var_list_find_items.append("\\" + item + " " + var_find_end)
    var_list_replace_items.append(item + var_replace_end)
    var_list_replace_items.append(item + " " + var_replace_end)
    # these ones look screwy - regex doesn't like missing 



def import_txt_file(input_path, output_path, list_find_items, list_replace_items):
    with open(input_path, "r", encoding='utf-8') as file_input:
        # read the file contents
        file_contents = file_input.read()
        var_max = len(list_find_items)
        
        file_contents = re.sub("ʼ", "'", file_contents)
        # because apparently the OCR did inconsistent interpretation of single-apostrophes
        # and ʼ confuses python unless I import uft-8, while ' is fine
        
        for i in range(var_max):
            file_contents = re.sub(list_find_items[i], list_replace_items[i], file_contents)
        with open(output_path, "w+") as file_output:
            file_output.write(file_contents)
            print(f"Created {output_path}")

def main():
    for i in range(var_number_of_files):
        import_txt_file(var_inputText_paths[i], var_RegexModdedText_paths[i], var_list_find_items, var_list_replace_items)
    print("Done")
main()

# 83
# 80
# 67
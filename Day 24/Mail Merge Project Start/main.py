import os

#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".

#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
#Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
#Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

# Set base path to this script's folder
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Define paths using os.path.join for portability
names_path = os.path.join(BASE_PATH, "Input", "Names", "invited_names.txt")
template_path = os.path.join(BASE_PATH, "Input", "Letters", "starting_letter.txt")
output_dir = os.path.join(BASE_PATH, "Output", "ReadyToSend")

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

fixed_names = []

# Read and clean names from the input file
with open(names_path, mode='r') as file:
    list_names = file.readlines()
    for name in list_names:
        modified_name = name.strip()
        fixed_names.append(modified_name)

# Read the letter template
with open(template_path, mode='r') as file:
    full_letter = file.readlines()

# Create a personalized letter for each name
for name in fixed_names:
    new_dear_name = full_letter[0].replace("[name],", f"{name},")
    result = new_dear_name + "".join(full_letter[1:])
    clean_result = result.strip()

    # Write the final letter to the output folder
    output_file = os.path.join(output_dir, f"letter_{name}.txt")
    with open(output_file, mode='w') as file:
        file.write(clean_result)

import os

try:
    os.mkdir("output_dir")
except FileExistsError:
    pass
try:
    os.mkdir("temp")
except FileExistsError:
    pass
try:
    os.mkdir("toy_output_dir")
except FileExistsError:
    pass

pa1_data_name = "pa1-data"
pa1_data_dir_list = sorted(os.listdir("pa1-data"))
pa1_data_dir_name = pa1_data_dir_list[0]
file_list = sorted(os.listdir(pa1_data_name + '\\' + pa1_data_dir_name))
file_name = file_list[0]
print(file_name)
file_path = os.path.join(pa1_data_name, pa1_data_dir_name, file_name)
with open(file_path, 'r') as file:
    print(file.read())
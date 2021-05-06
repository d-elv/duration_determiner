from pymediainfo import MediaInfo
import datetime
import re
import os
import io

"""
MATHS SECTION
1 second of DNxLB at 23.98fps: 4.33MB
1 second of DNxLB at 25fps: 4.51MB
1 second of DNxLB at 29.97fps: 5.41MB
1 minute of DNxLB at 23.98fps: 260MB
1 minute of DNxLB at 25fps: 271MB
1 minute of DNxLB at 29.97fps: 325MB
10 minutes of DNxLB at 23.98fps: 2.6GB
10 minutes of DNxLB at 25fps: 2.65GB
10 minutes of DNxLB at 29.97fps: 3.2GB
1 hour of DNxLB at 23.98fps: 15.22GB
1 hour of DNxLB at 25fps: 15.87GB
1 hour of DNxLB at 29.97fps: 19.02GB

1 second = 1000 milliseconds
10 seconds = 10000 milliseconds

1 second = 4330000 bytes at 23.98fps DNxLB
1 second = 4510000 bytes at 25fps DNxLB
1 second = 5410000 bytes at 29.97fps DNxLB

10 seconds = 43290000 at 23.98fps DNxLB
10 seconds = 43330000 at 24fps DNxLB
10 seconds = 45130000 at 25ps DNxLB
10 seconds = 54110000 at 29.97ps DNxLB
"""

LOG_DIRECTORY = "\\\\10.10.52.250\\dropzone\\CTA\\08 PYTHON PROGRAMS\\07_duration_determiner\\LOGGED_OUTPUT"

print("""Duration Determiner 
This program scans all subfolders given and
then finds the combined duration of all media files.
""")

single_dig_pattern = re.compile(r'\.[0-9]')
multi_dig_pattern = re.compile(r'([0-9]*)')
illegal_apostrophe = re.compile(r"'")
illegal_quotes = re.compile(r'"')
ghost_file_pattern = re.compile(r'^(\.)[<>-_.,+!?£$%^&*a-zA-Z0-9]*')
accepted_file_types = [
                    '.mov', 
                    '.mxf', 
                    '.avi', 
                    '.mp4', 
                    '.wmv', 
                    '.mkv',
                    '.m4v',
                    ]



def get_date():
    from datetime import datetime
    today = datetime.today().strftime('%Y%m%d')
    today = today[2:]
    return today


def get_root_length(input_directory):
    # Gets the root length of the directory given for scanning,
    # This is later used to ensure no sub folders are scanned.
    for root, dir_path, files in os.walk(input_directory):
        root_splitter = root.split("\\")
        folder_name_for_output_file = root_splitter[-1]
        root_length = len(root_splitter)

        return root_length, folder_name_for_output_file


def format_bit_rate(bit_rate_raw):
    if bit_rate_raw < (1000 * 1000):
        bit_rate_formatted = bit_rate_raw / 1000
        bit_rate_formatted = str(bit_rate_formatted)
        bit_rate_formatted = bit_rate_formatted[:-4] + " KB/s"
    if bit_rate_raw > (1000 * 1000):
        bit_rate_formatted = bit_rate_raw / (1000 * 1000)
        bit_rate_formatted = str(bit_rate_formatted)
        bit_rate_formatted = bit_rate_formatted[:-4] + " MB/s"


def format_milliseconds(file_duration_seconds):
    # formats duration from milliseconds to hours, minutes, seconds
    file_duration_milli = file_duration_seconds / 1000
    file_duration_milli = str(file_duration_milli)[-2:]
    
    if file_duration_milli == '.0':
        pass
    if single_dig_pattern.match(file_duration_milli):
        file_duration_milli = file_duration_milli + "0"
    else:
        file_duration_milli = '.' + str(file_duration_milli)
    
    file_duration_seconds = file_duration_seconds / 1000
    file_duration_seconds = int(file_duration_seconds)
    file_duration_formatted = str(datetime.timedelta(seconds=file_duration_seconds))
    file_duration_formatted = str(file_duration_formatted) + file_duration_milli

    hours = file_duration_formatted.split(":")
    hours = str(hours)[0]
    if len(hours) == 1:
        hours = "0"
    
    file_duration_formatted = hours + file_duration_formatted
        
    return file_duration_formatted        


def format_file_size(file_size):
    # formats file sizes from bytes so that they are easily readable
    if file_size > 1000000000:
        file_size = file_size / 1000000000
        file_size = str(file_size)
        file_size = file_size[:6] + "GB"
    elif file_size > 1000000:
        file_size = file_size / 1000000
        file_size = str(file_size)
        file_size = file_size[:6] + " MB"
    elif file_size > 1000:
        file_size = file_size / 1000
        file_size = str(file_size) + " KB"
    elif file_size < 1000:
        file_size = str(file_size) + " Bytes"

    return file_size


def predict_avid_size(combined_duration):
    twenty_three_nine_eight = 4329000
    twenty_four = 4333000
    twenty_five = 4513000
    twenty_nine_nine_seven = 5411000
    seconds = combined_duration / 1000

    twenty_three_nine_eight = seconds * twenty_three_nine_eight
    twenty_three_nine_eight = format_file_size(twenty_three_nine_eight)
    twenty_four = seconds * twenty_four
    twenty_four = format_file_size(twenty_four)
    twenty_five = seconds * twenty_five
    twenty_five = format_file_size(twenty_five)
    twenty_nine_nine_seven = seconds * twenty_nine_nine_seven
    twenty_nine_nine_seven = format_file_size(twenty_nine_nine_seven)

    return twenty_three_nine_eight, twenty_four, twenty_five, twenty_nine_nine_seven


while True:
    choice = ""
    root_length = 0
    folder_name_for_output_file = ""
    combined_duration = 0
    print('-'*60)
    print()

    input_directory = input('Please drag in a folder to scan the duration (or just provide seconds for quick maths): ')
    
    if illegal_apostrophe.search(input_directory):
        input_directory = input_directory.replace("'","")
    if illegal_quotes.search(input_directory):
        input_directory = input_directory.replace('"',"")

    if "/" not in input_directory and "\\" not in input_directory:
        input_directory = int(input_directory)
        combined_duration = input_directory
        combined_duration = combined_duration * 1000
        twenty_three_nine_eight, twenty_four, twenty_five, twenty_nine_nine_seven = predict_avid_size(combined_duration)
        print()
        print(f"Estimated DNxLB ingest size at 23.98fps based on duration: {twenty_three_nine_eight}")
        print(f"Estimated DNxLB ingest size at 24fps based on duration: {twenty_four}")
        print(f"Estimated DNxLB ingest size at 25fps based on duration: {twenty_five}")
        print(f"Estimated DNxLB ingest size at 29.97fps based on duration: {twenty_nine_nine_seven}\n")
        continue

    root_length, folder_name_for_output_file = get_root_length(input_directory)

    os.chdir(LOG_DIRECTORY)
    with open(folder_name_for_output_file + "_duration_determined.txt", "a") as log_file:
        log_file.write(f"FOLDER NAME: {folder_name_for_output_file}\n\n")

    def write_log():
        os.chdir(LOG_DIRECTORY)
        with io.open(folder_name_for_output_file + "_duration_determined.txt", "a", encoding="utf8") as log_file:
            for attribute in writing_to_file_list:
                log_file.write(str(attribute))
                log_file.write("\n")

    print("Scanning files... ")
    print("1", end="")
    file_count = 0
    error_count = 0
    for root, dir_path, files in os.walk(input_directory):
        for file in files:
            
            file_name, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext not in accepted_file_types:
                continue

            writing_to_file_list = []
            
            current_root_split = root.split("\\")
            
            if ghost_file_pattern.match(file):
                continue

            file_path = os.path.join(root, file)

            try:
                file_media_info = MediaInfo.parse(file_path)
            except FileNotFoundError:
                print("Your file path is incorrect or your filename ", end="")
                print("is missing its extension, please try again. ")
                
                break
            
            for track in file_media_info.tracks:
                if track.track_type == "General":

                    file_name = track.complete_name
                    file_name = file_name.replace('\\', '/')
                    file_name = file_name.split('/')
                    file_name = file_name[-1]

                    current_file_path = track.complete_name
                    
                    file_size_raw = track.file_size
                    file_duration_milliseconds = track.duration

                    if file_duration_milliseconds == None:
                        print(f"{file_name} is a corrupt file, please ", end="")
                        print(f"investigate, resupply and try scanning again.")
                    else:
                        combined_duration += file_duration_milliseconds

                    if track.file_size == 0 or track.file_size == None:
                        print(f"{file_name} is a corrupt file, please ", end="")
                        print(f"investigate, resupply and try scanning again.")
                        error_count += 1
                        break
                    else:
                        pass
            file_count += 1
            print("\r%d"%file_count, end="")

    twenty_three_nine_eight, twenty_four, twenty_five, twenty_nine_nine_seven = predict_avid_size(combined_duration)
    format_duration = format_milliseconds(combined_duration)

    with open(folder_name_for_output_file + "_duration_determined.txt", "a") as log_file:
        log_file.write("\n")
        log_file.write(f"Duration formatted as: HH:MM:SS.Milliseconds\n")
        log_file.write(f"Total duration of selection: {format_duration}\n")
        log_file.write("\n")
        log_file.write(f"Estimated DNxLB ingest size at 23.98fps based on duration: {twenty_three_nine_eight}\n")
        log_file.write(f"Estimated DNxLB ingest size at 24fps based on duration: {twenty_four}\n")
        log_file.write(f"Estimated DNxLB ingest size at 25fps based on duration: {twenty_five}\n")
        log_file.write(f"Estimated DNxLB ingest size at 29.97fps based on duration: {twenty_nine_nine_seven}\n")
        log_file.write("\n")
        log_file.write(f"Total media files in selection: {file_count}\n")
        log_file.write("\n")

    print(f"\nYour selection's aggregate duration is {format_duration}\n")
    print(f"Estimated DNxLB ingest size at 23.98fps based on duration: {twenty_three_nine_eight}")
    print(f"Estimated DNxLB ingest size at 24fps based on duration: {twenty_four}")
    print(f"Estimated DNxLB ingest size at 25fps based on duration: {twenty_five}")
    print(f"Estimated DNxLB ingest size at 29.97fps based on duration: {twenty_nine_nine_seven}\n")
    print(f"\nThis has been written to a text log here: {LOG_DIRECTORY}")
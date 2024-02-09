import re
import sys
import os

def parse_xml(xml_file):
    with open(xml_file, 'r') as f:
        xml_data = f.read()
    data_start = xml_data.find('<Data>') + len('<Data>')
    data_end = xml_data.find('</Data>')
    data_section = xml_data[data_start:data_end]
    lines = data_section.split('\n')
    notes = []
    for line in lines:
        if line.strip():
            notes.append(line.strip())
    return notes

def transform_notes(notes, res):
    transformed_notes = []
    print("\n!!!\nNo matter how much you try to fix a freetar (sng/xml) chart, it will never be good.\nConsider charting from scratch instead.\nCheck out Moonscraper Chart Editor: https://github.com/FireFox2000000/Moonscraper-Chart-Editor\n!!!\n")
    print("\nDebug Info")
    for i, note in enumerate(notes):
        time_match = re.search(r'time="([^"]+)"', note)
        duration_match = re.search(r'duration="([^"]+)"', note)
        track_match = re.search(r'track="([^"]+)"', note)
        if time_match and duration_match and track_match:
            time = float(time_match.group(1))
            duration = float(duration_match.group(1))
            track = int(track_match.group(1))
            new_time = round(time * (res * 2))
            new_duration = round(duration * (res * 2))
            transformed_notes.append(f'{new_time} = N {track} {new_duration}')
            if i < 10:
                print(f"Iteration {i+1}: time={time}, duration={duration}, track={track} => new_time={new_time}, new_duration={new_duration}")
    print()
    return transformed_notes

def write_chart(transformed_notes, output_file, res):
    with open(output_file, 'w') as f:
        f.write(f"[Song]\n{{\n  Name = \"No matter what you\"\n  Artist = \"do, a freetar sng will\"\n  Charter = \"always be bad. chart\"\n  Album = \"from scratch instead.\"\n  Year = \", 2024\"\n  Offset = 0\n  Resolution = {res}\n  Player2 = bass\n  Difficulty = 2\n  PreviewStart = 0\n  PreviewEnd = 0\n  Genre = \"-Naonemeu\"\n  MediaType = \"cd\"\n}}\n")
        f.write("[SyncTrack]\n{\n  0 = TS 4\n  0 = B 120000\n}\n")
        f.write("[Events]\n{\n}\n")
        f.write("[ExpertSingle]\n{\n")
        for note in transformed_notes:
            f.write(note + '\n')
        f.write("}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if input_file.lower().endswith(('.chart', '.mid')):
            print("Do not use a .chart or .mid file as an input (Overwrite prevention)")
            input("Press Enter to exit...")
            sys.exit(1)
        res = 480
        file_name, _ = os.path.splitext(input_file)
        output_file = f"{file_name}.chart"
        notes = parse_xml(input_file)
        transformed_notes = transform_notes(notes, res)
        write_chart(transformed_notes, output_file, res)
        print(f"Output file '{output_file}' has been generated.")
    else:
        xml_file = input("Enter the path to the XML file: ")
        output_file = input("Enter the desired name for the output chart file (with .chart extension): ")
        if output_file.lower().endswith(('.chart', '.mid')):
            print("Do not use a .chart or .mid file as an output (Overwrite prevention)")
            input("Press Enter to exit...")
            sys.exit(1)
        res = 480
        notes = parse_xml(xml_file)
        transformed_notes = transform_notes(notes, res)
        write_chart(transformed_notes, output_file, res)
        print(f"Output file '{output_file}' has been generated.")
    input("Press Enter to exit...")

import xml.etree.ElementTree as ET
from common import get_filename

# Define the root element
score_partwise = ET.Element("score-partwise", version="3.1")

# Add a part list
part_list = ET.SubElement(score_partwise, "part-list")
score_part = ET.SubElement(part_list, "score-part", id="P1")
part_name = ET.SubElement(score_part, "part-name")
part_name.text = "Piano"

# Add a part
part = ET.SubElement(score_partwise, "part", id="P1")

# Add measures
measure = ET.SubElement(part, "measure", number="1")

# Add notes
note_elem = ET.SubElement(measure, "note")
pitch = ET.SubElement(note_elem, "pitch")
step = ET.SubElement(pitch, "step")
step.text = "C"
octave = ET.SubElement(pitch, "octave")
octave.text = "4"
duration = ET.SubElement(note_elem, "duration")
duration.text = "1"

# Get the file name
filename = get_filename(ext='xml', user_input=False, prefix='xmltree')

# Write to a MusicXML file
tree = ET.ElementTree(score_partwise)
with open(f"output/{filename}", "wb") as f:
    tree.write(f)

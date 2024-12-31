import os
import xml.etree.ElementTree as ET

def process_event(event):
    # Extract the current concept:name value
    concept_name_element = event.find(".//{*}string[@key='concept:name']")
    if concept_name_element is None:
        return

    concept_value = concept_name_element.attrib['value']

    # Parse the concept:name value
    parts = concept_value.split(", ")
    
    # Extract specific parts of the name based on assumed format
    name = parts[0] if len(parts) > 1 else "Unknown"
    location = parts[1] if len(parts) > 1 else "Unknown"
    activity = parts[2] if len(parts) > 2 else "Unknown"

    # Update the XML structure
    ET.SubElement(event, 'string', key='location', value=location)
    ET.SubElement(event, 'string', key='activity', value=activity)
    
    # Update the concept:name value
    concept_name_element.attrib['value'] = f"{name}"

def process_xes_file(input_file, output_file):
    # Parse the input XES file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Remove namespaces to avoid ns0 prefix
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]  # Remove namespace
        if elem.attrib:
            for key in list(elem.attrib):
                if '}' in key:
                    new_key = key.split('}', 1)[1]
                    elem.attrib[new_key] = elem.attrib.pop(key)

    # Process each event in the XES file
    for event in root.findall(".//event"):
        process_event(event)

    # Write the modified XML to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def process_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each XES file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".xes"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            process_xes_file(input_file, output_file)


if __name__ == "__main__":
    input_folder = "./06_Sub-Process_S01"  # Replace with your input folder path
    output_folder = "./06_Sub-Process_S01"  # Replace with your output folder path
    process_folder(input_folder, output_folder)

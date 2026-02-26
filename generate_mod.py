import os
import sys
import shutil
import copy
from lxml import etree

def get_files_recursively(path, extension='.sbc'):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(extension):
                result.append(os.path.join(root, file))
    return result

def normalize_xml(xml):
    text = etree.tostring(xml).decode('utf-8')
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.fromstring(text, parser=parser)

def generate_dlc_hiding(se_path, filter_list):
    data_path = os.path.join(se_path, 'Content', 'Data')
    files = get_files_recursively(data_path, '.sbc')

    # collect tuples of (parent_tag, element_copy)
    hidden_items = []
    audit_log = {} 

    for file_path in files:
        try:
            tree = etree.parse(file_path)
            for item in tree.xpath('//Definition'): 
                dlc_tag = item.find('DLC')
                
                if dlc_tag is not None:
                    dlc_name = dlc_tag.text
                    if dlc_name in filter_list:
                        continue
                    
                    item_id = item.find('Id/SubtypeId')
                    item_name = item_id.text if item_id is not None else "Unknown"

                    public_tag = item.find('Public')
                    if public_tag is None:
                        public_tag = etree.SubElement(item, 'Public')
                    public_tag.text = 'false'
                    
                    # copy the item to avoid repeating issues and preserve original parent tag
                    parent = item.getparent()
                    parent_tag = parent.tag if parent is not None else 'CubeBlocks'
                    hidden_items.append((parent_tag, copy.deepcopy(item)))

                    if dlc_name not in audit_log:
                        audit_log[dlc_name] = 0
                    audit_log[dlc_name] += 1
        except Exception:
            continue

    print("\n| DLC Name | Items Hidden |")
    print("| :--- | :--- |")
    for dlc, count in sorted(audit_log.items()):
        print(f"| {dlc} | {count} |")
    
    print(f"\nTotal_Items_Hidden: {len(hidden_items)}")
    
    dlc_hide_xml = etree.Element('Definitions', nsmap={
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsd': 'http://www.w3.org/2001/XMLSchema'
    })
    # group copied items by their original parent tag and append under matching containers
    groups = {}
    for parent_tag, elem in hidden_items:
        if parent_tag not in groups:
            groups[parent_tag] = etree.SubElement(dlc_hide_xml, parent_tag)
        groups[parent_tag].append(elem)
    
    return etree.ElementTree(normalize_xml(dlc_hide_xml))

def generate_local_mod(mod_path, mod_name, xml):
    os.makedirs(os.path.join(mod_path, 'Data'), exist_ok=True)
    data_path = os.path.join(mod_path, 'Data', 'CubeBlocks_Hidden.sbc')
    with open(data_path, 'wb') as f:
        f.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding='utf-8'))
    # Some older variants expect a differently named file; write a duplicate with that name
    alt_path = os.path.join(mod_path, 'Data', 'CubeBlocks_hider.sbc')
    try:
        shutil.copyfile(data_path, alt_path)
    except Exception:
        pass

    # Copy an existing `modinfo.sbc`
    possible_sources = [
        os.path.join(os.path.dirname(__file__), 'modinfo.sbc'),
        os.path.join(os.getcwd(), 'modinfo.sbc'),
    ]

    # Ensure mod root exists
    os.makedirs(mod_path, exist_ok=True)
    modinfo_path = os.path.join(mod_path, 'modinfo.sbc')
    copied = False
    for src in possible_sources:
        if os.path.exists(src):
            try:
                shutil.copyfile(src, modinfo_path)
                print(f"Copied modinfo from: {src}")
                copied = True
                break
            except Exception as e:
                print(f"Warning: failed to copy modinfo from {src}: {e}")

    if not copied:
        print("Note: no modinfo.sbc found next to the script or in CWD; skipping modinfo creation.")

    print(f"Mod_Generated_At: {mod_path}")

if __name__ == '__main__':
    mod_name = 'DLCBlocksHider'
    mod_path = os.path.join(os.path.expandvars(r'%APPDATA%\SpaceEngineers\Mods'), mod_name)
    
    # Check for --test flag anywhere in arguments
    is_test = "--test" in sys.argv
    # Filter out the script name and the --test flag to find the path
    args = [a for a in sys.argv[1:] if a != "--test"]

    # 1. Try to get path from argument
    if len(args) >= 1:
        se_path = args[0].strip('"')
    else:
        # 2. Fallback to interactive input
        se_path = input('Please write your SpaceEngineers folder path: (Press Ctrl+C to exit)\n> ').strip('"')

    # 3. Path Validation
    if not se_path:
        print("Error: No path provided.")
        sys.exit(1)

    exe_check = os.path.join(se_path, "Bin64", "SpaceEngineers.exe")
    if not os.path.exists(exe_check):
        print(f"Error: Invalid Space Engineers path. Could not find: {exe_check}")
        sys.exit(1)
    
    # Run the generator
    dlc_hide_xml = generate_dlc_hiding(se_path, [])
    
    if is_test:
        print("\nTest_Mode_Enabled: No files were written.")
    else:
        generate_local_mod(mod_path, mod_name, dlc_hide_xml)
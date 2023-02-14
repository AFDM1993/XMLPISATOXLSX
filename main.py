import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('pisa_results.xml')
root = tree.getroot()

header = ['STRUCTURE', 'HSDC', 'SOLVENTACCESSIBLEAREA', 'BURIEDSURFACEAREA', 'BURIEDSURFACEAREASCORE', 'SOLVATIONENERGY']

if len(root) == 0:
    raise Exception("No data found in the XML file")

# Create a list of dictionaries to store the data
data = []

# Iterate over the residues
for residue in root.iter('RESIDUE'):
    res_data = {}
    structure, residue_number = residue.find('STRUCTURE').text.strip().split()
    res_data['Amino Acid'] = structure
    res_data['Residue Number'] = residue_number
    res_data['HSDC'] = residue.find('HSDC').text.strip()
    res_data['Solvent Accessible Area'] = residue.find('SOLVENTACCESSIBLEAREA').text.strip()
    res_data['Buried Surface Area'] = residue.find('BURIEDSURFACEAREA').text.strip()
    res_data['Buried Surface Area Score'] = residue.find('BURIEDSURFACEAREASCORE').text.strip()
    res_data['Solvation Energy'] = residue.find('SOLVATIONENERGY').text.strip()
    data.append(res_data)

# Create a pandas dataframe from the list of dictionaries
df = pd.DataFrame(data)

# Write the dataframe to an excel file
df.to_excel('aminoacid_data.xlsx', index=False)

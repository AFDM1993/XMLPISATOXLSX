import xml.etree.ElementTree as ET 
import pandas as pd 

# Define a translation dictionary for converting 3-letter code to 1-letter code
trans = {'CYS':'C', 'ASP':'D', 'SER':'S', 'GLN':'Q', 'LYS':'K', 'ILE':'I', 'PRO':'P', 'THR':'T', 'PHE':'F', 'ASN':'N', 'GLY':'G', 'HIS':'H', 'LEU':'L', 'ARG':'R', 'TRP':'W', 'ALA':'A', 'VAL':'V', 'GLU':'E', 'TYR':'Y', 'MET':'M'}

tree = ET.parse('HaddockScfvCD19CDRC11s08residue.xml') 
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
    res_data['Amino Acid'] = structure[0] 
    res_data['Residue Number'] = residue_number 
    res_data['HSDC'] = residue.find('HSDC').text.strip() 
    res_data['Solvent Accessible Area'] = residue.find('SOLVENTACCESSIBLEAREA').text.strip() 
    res_data['Buried Surface Area'] = residue.find('BURIEDSURFACEAREA').text.strip() 
    res_data['Buried Surface Area Score'] = residue.find('BURIEDSURFACEAREASCORE').text.strip() 
    res_data['Solvation Energy'] = residue.find('SOLVATIONENERGY').text.strip() 
    res_data['3-letter Code'] = structure.split(':')[1].strip()
    data.append(res_data) 

# Create a pandas dataframe from the list of dictionaries 
df = pd.DataFrame(data, columns=['Amino Acid', '3-letter Code', 'Residue Number', 'HSDC', 'Solvent Accessible Area', 'Buried Surface Area', 'Buried Surface Area Score', 'Solvation Energy']) 

# Add a new column to the dataframe to keep the 1-letter code
df['1-letter Code'] = df['3-letter Code'].map(trans)

# Write the dataframe to an excel file 
with pd.ExcelWriter('aminoacid_data.xlsx') as writer:
    df[df['Amino Acid'] == 'A'].to_excel(writer, sheet_name='SheetA', index=False)
    df[df['Amino Acid'] == 'B'].to_excel(writer, sheet_name='SheetB', index=False)

# coding=utf-8

# inputfile = mmod_csearch.mae [ligand with simple minimization, but not binding pose] 
#             macromodel embrace write file(.mae and .com), get from schrodinger Embrace Minimization model (Interaction energy mode) by ligand binding pose and protein
# How to use: python MM-GBSA_Rescoring.py


import numpy as np
import os
import subprocess
import time
import re


# Check whether there are any files starting with "mmod_csearch" under the current folder
file_name_l = [f for f in os.listdir('.') if f.startswith('mmod_csearch') and f.endswith('.mae')]
if len(file_name_l) == 0:
    print("Input file for mmod_csearch was not found")
    exit()

# Create a mmod_csearch.com file
csearch_file = "mmod_csearch.com"

file_1 = open(csearch_file, 'w')

content = """mmod_csearch.mae
mmod_energy.mae
 MMOD       0      1      0      0     0.0000     0.0000     0.0000     0.0000
 DEBG      55      0      0      0     0.0000     0.0000     0.0000     0.0000
 FFLD      14      1      0      0     1.0000     0.0000     0.0000     0.0000
 SOLV       3      1      0      0     0.0000     0.0000     0.0000     0.0000
 EXNB       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 BDCO       0      0      0      0    89.4427 99999.0000     0.0000     0.0000
 READ       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 CRMS       0      0      0      0     0.0000     0.3000     0.0000     2.0000
 MCMM    1000      0      0      0     0.0000     0.0000     0.0000     0.0000
 NANT       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 MCNV       1      5      0      0     0.0000     0.0000     0.0000     0.0000
 MCSS       2      0      0      0    21.0000     0.0000     0.0000     0.0000
 MCOP       1      0      0      0     0.0000     0.0000     0.0000     0.0000
 DEMX       0    833      0      0    21.0000    42.0000     0.0000     0.0000
 MSYM       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 AUOP       0      0      0      0   100.0000     0.0000     0.0000     0.0000
 AUTO       0      2      1      1     0.0000     1.0000     0.0000     3.0000
 CONV       2      0      0      0     0.0500     0.0000     0.0000     0.0000
 MINI       1      0   2500      0     0.0000     0.0000     0.0000     0.0000

"""

file_1.write(content)
file_1.close()

# Create a mmod_energy.com file
energy_file = "mmod_energy.com"

file_2 = open(energy_file, 'w')

content_2 = """mmod_energy.mae
mmod_energy-out.mae
 MMOD       0      1      0      0     0.0000     0.0000     0.0000     0.0000
 FFLD      14      1      0      0     1.0000     0.0000     0.0000     0.0000
 SOLV       3      1      0      0     0.0000     0.0000     0.0000     0.0000
 EXNB       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 BDCO       0      0      0      0    89.4427 99999.0000     0.0000     0.0000
 BGIN       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 READ      -1      0      0      0     0.0000     0.0000     0.0000     0.0000
 ELST      -1      0      0      0     0.0000     0.0000     0.0000     0.0000
 WRIT       0      0      0      0     0.0000     0.0000     0.0000     0.0000
 END       0      0      0      0     0.0000     0.0000     0.0000     0.0000

"""

file_2.write(content_2)
file_2.close()

def check_command_completion(log_file, target_word):
    # Check that the last word of the last line of the log file is the target word
    with open(log_file, "r") as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            last_word = last_line.split()[-1]
            return last_word == target_word
        else:
            return False

def run_command(command):
    subprocess.run(command, shell=True)

# First command
command1 = "bmin mmod_csearch"
log_file1 = "mmod_csearch.log"
target_word1 = "total"

run_command(command1)

while not check_command_completion(log_file1, target_word1):
    time.sleep(5)   # Wait five seconds before checking

# Second command
command2 = "bmin mmod_energy"
log_file2 = "mmod_energy.log"

run_command(command2)

while not check_command_completion(log_file2, target_word1):
    time.sleep(5)

print("mmod_csearch and mmod_energy have done")


# Gets the file name under the current folder that starts with "mmod_energy"
file_name = [f for f in os.listdir('.') if f.startswith('mmod_energy') and f.endswith('.log')]
if len(file_name) == 0:
    print("No files starting with 'mmod_energy' were found")
    exit()

# Read mmod_energy.log file and extract Total Energy
Ei_list = []
with open(file_name[0], 'r') as f:
    lines1 = f.readlines()
    for line1 in lines1:
        if 'Total Energy =' in line1:
            Ei = float(line1.split()[3])
            Ei_list.append(Ei)

# Read mmod_energy.log file and extract Solvation
Gs_list = []
with open(file_name[0], 'r') as f:
    lines2 = f.readlines()
    for line2 in lines2:
        if 'Solvation =' in line2:
            Gs = float(line2.split()[2])
            Gs_list.append(Gs)

k = 1.380649e-23 # Boltzmann constant in units J/K
T = 300 # Temperature in K

# Calculate the probability Pi for each conformation
Pi_list=[]
for E in Ei_list:
    Pi = np.exp(max(-700, min(-E / (k * T), 700))) / sum([np.exp(max(-700, min(-E / (k * T), 700))) for E in Ei_list])
    Pi_list.append(Pi)

# Calculate Ei_U and Gs_U
Ei_U = sum([Pi*Ei for Pi, Ei in zip(Pi_list, Ei_list)])
Gs_U = sum([Pi*Gs for Pi, Gs in zip(Pi_list, Gs_list)])

# Calculate S_conf and TdS
k_b = k
S_conf = (-k_b) * sum([Pi * np.log(Pi) for Pi in Pi_list])
S_conf = float(S_conf)
TdS = (0 - S_conf) * T

print('S_conf =', S_conf)

Ei_U_kcal = Ei_U * 0.239
Gs_U_kcal = Gs_U * 0.239
TdS_kcal = TdS * 0.239

with open('MM-GBSA_recoring.txt', 'w') as f:
    f.write(f'Ei_U: {Ei_U_kcal} kcal/mol\n')
    f.write(f'Gs_U: {Gs_U_kcal} kcal/mol\n')
    f.write(f'S_conf: {S_conf}\n')
    f.write(f'TdS: {TdS_kcal} kcal/mol')


# Calculate embrace minimization
# Gets the file name that starts with "mmod_mbaemini" under the current folder
file_name_p = [f for f in os.listdir('.') if f.startswith('mmod_mbaemini') and f.endswith('.com')]
if len(file_name_p) == 0:
    print("Files starting with 'mmod_mbaemini' were not found")
    exit()

# Read the contents of the file, delete the third line and add a new line after the FFLD
with open(file_name_p[0], 'r') as f:
    lines = f.readlines()

del lines[2]

lines.insert(3, ' SOLV       3      1      0      0     0.0000     0.0000     0.0000     0.0000\n')

with open(file_name_p[0], 'w') as f:
    f.writelines(lines)

# Get the file name (without suffix)
file_name_p_without_extension, _ = os.path.splitext(file_name_p[0])

# Execute the command
command = f"bmin {file_name_p_without_extension}"
os.system(command)

log_file_name_p = file_name_p_without_extension + ".log"

# Check whether the task is complete and whether the log file is complete
while not check_command_completion(log_file_name_p, target_word1):
    time.sleep(5)

# Open the log file and read its contents
with open(log_file_name_p, 'r') as f:
    content = f.read()

# Find Total Energy, Solvation SA, Solvation GB, Compute E_ptn after Atom set 1
total_energy_line1 = content.split('Atom set   1:\n')[1].split('\n')[0]
total_energy_value1 = re.sub(r'\s*\([^)]*\)', '', total_energy_line1.split('=')[1]).strip()

solvation_sa_line1 = content.split('Atom set   1:\n')[1].split('\n')[7]
solvation_sa_value1 = re.sub(r'\s*\([^)]*\)', '', solvation_sa_line1.split('=')[1]).strip()

solvation_gb_line1 = content.split('Atom set   1:\n')[1].split('\n')[8]
solvation_gb_value1 = re.sub(r'\s*\([^)]*\)', '', solvation_gb_line1.split('=')[1]).strip()

total_energy_value1 = float(total_energy_value1)
solvation_sa_value1 = float(solvation_sa_value1)
solvation_gb_value1 = float(solvation_gb_value1)
E_ptn = total_energy_value1 - solvation_sa_value1 - solvation_gb_value1

# Find Solvation SA and Solvation GB after Atom Set 2 to calculate Gs_B; Find Total Energy calculation Ei_B
solvation_sa_line2 = content.split('Atom set   2:\n')[1].split('\n')[7]
solvation_sa_value2 = re.sub(r'\s*\([^)]*\)', '', solvation_sa_line2.split('=')[1]).strip()
solvation_gb_line2 = content.split('Atom set   2:\n')[1].split('\n')[8]
solvation_gb_value2 = re.sub(r'\s*\([^)]*\)', '', solvation_gb_line2.split('=')[1]).strip()

solvation_sa_value2 = float(solvation_sa_value2)
solvation_gb_value2 = float(solvation_gb_value2)
Gs_B = solvation_sa_value2 + solvation_gb_value2

total_energy_line2 = content.split('Atom set   2:\n')[1].split('\n')[0]
total_energy_value2 = re.sub(r'\s*\([^)]*\)', '', total_energy_line2.split('=')[1]).strip()

total_energy_value2 = float(total_energy_value2)
Ei_B = total_energy_value2 - Gs_B

# Find Van der Waals and Electrostatic after Atom Sets 1 and 2 and extract their values
van_der_waals = re.search(r'Atom sets   1 and   2:\n.*\n.*Van der Waals =\s+(-?\d+\.\d+)', content, re.DOTALL)
electrostatic = re.search(r'Atom sets   1 and   2:\n.*\n.*Electrostatic =\s+(-?\d+\.\d+)', content, re.DOTALL)

E_vdw = van_der_waals.group(1)
E_elect = electrostatic.group(1)

Gs_B_kcal = Gs_B * 0.239
Ei_B_kcal = Ei_B * 0.239
E_vdw_kcal = float(E_vdw) * 0.239
E_elect_kcal = float(E_elect) * 0.239
E_ptn_kcal = E_ptn * 0.239

# Write the extracted Total Energy and Solvation SA values to a new log.txt file
with open('MM-GBSA_recoring.txt', 'a') as f:
    f.write(f'\nGs_B: {Gs_B_kcal} kcal/mol\n')
    f.write(f'Ei_B: {Ei_B_kcal} kcal/mol\n')
    f.write(f'E_vdw: {E_vdw_kcal} kcal/mol\n')
    f.write(f'E_elect: {E_elect_kcal} kcal/mol\n')
    f.write(f'E_ptn: {E_ptn_kcal} kcal/mol')

print("mmod_embrace have done")

dEi_kcal = Ei_B_kcal - Ei_U_kcal
dGs_kcal = Gs_B_kcal - Gs_U_kcal

# MM-GB/SA rescoring Final calculation formula
dG_bind = dEi_kcal + dGs_kcal - TdS_kcal + E_vdw_kcal + E_elect_kcal + E_ptn_kcal

with open('MM-GBSA_recoring.txt', 'a') as f:
    f.write(f'\ndEi: {dEi_kcal} kcal/mol\n')
    f.write(f'dGs: {dGs_kcal} kcal/mol\n')
    f.write(f'dG_bind: {dG_bind} kcal/mol')

print("MM-GB/SA Rescoring have done, dG_bind: ", dG_bind, "kcal/mol")
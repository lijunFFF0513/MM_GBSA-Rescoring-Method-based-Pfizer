# MM_GBSA-Rescoring-Method-based-Pfizer
This calculation protocol is based on the following two literature：
1. Guimarães, C.R.W. (2012). MM-GB/SA Rescoring of Docking Poses. In: Baron, R. (eds) Computational Drug Discovery and Design. Methods in Molecular Biology, vol 819. Springer, New York, NY.
2. J. Chem. Inf. Model. 2008, 48, 5, 958–970.
# Principle of Calculation
![image](https://github.com/lijunFFF0513/MM_GBSA-Rescoring-Method-based-Pfizer/assets/109940009/8bc822c7-3bfc-4c9c-b698-d460d92a410b)
# Usage
1. You need to prepare the system, ligands and protein you want to calculate, and follow the Schrödinger Maestro processing protocol when preparing.
2. Name your ligands as "mmod_csearch.mae", which is bulit and simple optimized in Maestro. Save in the .py file directory.
3. Docking your ligands into the protein (or any other way, just put it into the protein).
4. Use your pose file as the input of 'Embrace Minimization' (MacroModel), Some settings can be modified as shown in the image：
![image](https://github.com/lijunFFF0513/MM_GBSA-Rescoring-Method-based-Pfizer/assets/109940009/2d4c4779-7ec0-4b91-8cb7-5e1e4d716eb9)![image](https://github.com/lijunFFF0513/MM_GBSA-Rescoring-Method-based-Pfizer/assets/109940009/94981659-4b90-406e-bfea-1d31e1f3ba4c)![image](https://github.com/lijunFFF0513/MM_GBSA-Rescoring-Method-based-Pfizer/assets/109940009/461a52b4-b972-430e-8010-ff936c8c01da)
   and 'Substructure' you can define by yourself. Finally, you need to 'write' these settings to a configuration folder, and finally get .com, .mae, .sbc files, and copy them to the .py file directory.
5. Enter the command "python MM-GBSA_Rescoring.py" in the terminal to run the script. The results are list in the MM-GBSA_recoring.txt

# ATTENTION！
1. To run this script you need a MacroModel license.
2. At present, this script only supports a single ligand, and will be optimized into a multiligand version in the future.
3. The problem of excessive E_ptn values in this calculation protocol still needs to be solved.

If you have any questions, you can contact [ j305631@outlook.com ]

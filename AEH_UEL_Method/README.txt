General procedures for predicting thermo-mechanical properties of composistes
using the UEL scheme of the AEH method:

(1). Generate RVEs of composites;

(2). Run the python script "Preprocessing_AEH_FEH.py" to conduct preprocess of the analysis 
and to generate a input file;

(3). Run the script "AEH_Inp_Periodic_BCs_Type_UEL.py" to process the generated input 
file at Step-2 to generated a new input file (Here Type = Elastic, ETC, CTE);

(4). Run the script "UEL_Inp_Modification_Type_UEL.py" to process the generated input 
file at Step-3 to generated a new input file;

(5). Conduct one FE analysis based on the generated input file at Step-4 and using the written
subroutine UEL;

(6). Run the script "DatFile_Processing_Type_UEL.py" to modify the generated dat file at Step-5;

(7). Run the script "AEH_Postprocessing_Type_UEL.py" to obtain the homogenized thermo-mechanical 
properties of composites.
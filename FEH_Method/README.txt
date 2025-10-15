General procedures for predicting thermo-mechanical properties of composistes
using the FEH method:

(1). Generate RVEs of composites;

(2). Run the python script "Preprocessing_AEH_FEH.py" to conduct preprocess of the analysis 
and to generate a input file;

(3). Run the script "FEH_Inp_Periodic_BCs_Type.py" to process the generated input 
file at Step-2 to generated a new input file (Here Type = Elastic, ETC, CTE1, CTE2);

(4). Conduct one FE analysis based on the generated input file at Step-3;

(5) Run the script "FEH_Postprocessing_Type.py" to obtain the homogenized thermo-mechanical 
properties of composites.
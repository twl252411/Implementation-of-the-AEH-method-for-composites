General procedures for predicting thermo-mechanical properties of composistes
using the Cheng's scheme of the AEH method:

(1). Generate RVEs of composites;

(2). Run the python script "Preprocessing_AEH_FEH.py" to conduct preprocess of the analysis 
and to generate a input file;

(3). Run the script "AEH_Inp_Preprocessing_Type_Cheng_s1.py" to process the generated input 
file at Step-2 to generated a new input file (Here Type = Elastic, ETC, CTE);

(4). Conduct one FE analysis based on the generated input file at Step-3, and then run the script
"AEH_Postprocessing_Type_Cheng_s1.py" to obtain the result data;

(5). Run the script "AEH_Inp_Preprocessing_Type_Cheng_s2.py" to process the generated input 
file at Step-2 and the result data at Step-4 to generated a new input file;

(6). Conduct one FE analysis based on the generated input file at Step-5, and then run the script
"AEH_Postprocessing_Type_Cheng_s2.py" to obtain the result data;
 
(7). Run the script "AEH_Inp_Preprocessing_Type_Cheng_s3.py" to process the generated input 
file at Step-2 and the result data at Step-6 to generated a new input file;

(8). Conduct one FE analysis based on the generated input file at Step-7, and then run the script
"AEH_Postprocessing_Type_Cheng_s4.py" to obtain the homogenized thermo-mechanical properties of composites.

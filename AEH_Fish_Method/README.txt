General procedures for predicting thermo-mechanical properties of composistes
using the Fish's scheme of the AEH method:

(1). Generate RVEs of composites;

(2). Run the python script "Preprocessing_AEH_FEH.py" to conduct preprocess of the analysis 
and to generate a input file;

(3). Run the script "AEH_Inp_Periodic_BCs_Elastic_Fish.py" to process the generated input 
file at Step-2 to generated a new input file;

(4). Conduct one FE analysis based on the generated input file at Step-3;

(5). Run the script "AEH_Postprocessing_Elastic_Fish.py" to obtain the homogenized elastic
properties of composites.
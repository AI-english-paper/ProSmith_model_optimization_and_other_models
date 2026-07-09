# ProSmith_model_optimization_and_other_models

*upload juiste files
## REQUIREMENTS
```text
Before running this workflow, make sure the following requirements are available:

-Python 3.8
-Micromamba or Conda
-Jupyter Notebook or JupyterLab
-Access to the ProSmith repository
-Access to the FusionESP repository
-Access to the required datasets and model files
``` 
## 1. Project Overview
### 1.1 Aim of this repository
### 1.2 Models included in this repository
### 1.3 General workflow order
### 1.4 Repository structure

## 2. ProSmith environment setup
### 2.1 Purpose of the standard ProSmith workflow
### 2.2 Required files and folders
### 2.3 Creating the ProSmith environment
### 2.4 Preparing the original ProSmith database
### 2.5 Expanding the ProSmith database
### 2.6 Preprocessing the expanded database
### 2.7 Creating train, validation, and test files
### 2.8 Generating protein and SMILES embeddings
### 2.9 Training the ProSmith transformer model
### 2.10 Training the Gradient Boosting model
### 2.11 Mapping predictions back to the test set
### 2.12 Expected output files
   
## 3. No-Leakage model setup
### 3.1 Purpose of the no-leakage workflow
### 3.2 Reused files and steps from the standard ProSmith workflow
### 3.3 Required no-leakage files and folders
### 3.4 Expanding the no-leakage database
### 3.5 Creating the no-leakage train, validation, and test split
### 3.6 Checking the no-leakage split
### 3.7 Generating no-leakage embeddings
### 3.8 Training the no-leakage ProSmith transformer model
### 3.9 Training the no-leakage Gradient Boosting model
### 3.10 Saving no-leakage predictions
### 3.11 Mapping no-leakage predictions back to the test set
### 3.12 Expected output files

## 4. FusionESP predictor setup
### 4.1 Purpose of the FusionESP predictor
### 4.2 Required files and folders
### 4.3 Setting up the FusionESP environment
### 4.4 Preparing FusionESP input data
### 4.5 Running the FusionESP predictor
### 4.6 Evaluating FusionESP prediction output
### 4.7 Expected output files



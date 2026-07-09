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

## 2. Shared environment setup

### 2.1 Creating or activating the environment
### 2.2 Installing dependencies
### 2.3 Navigating to the project repositories
### 2.4 Checking required datasets and model files
### 2.5 Testing the environment

## 3. Standard ProSmith workflow

### 3.1 Purpose of the standard ProSmith workflow
### 3.2 Required ProSmith files and folders
### 3.3 Preparing the original ProSmith database
### 3.4 Expanding the ProSmith database
### 3.5 Preprocessing the expanded database
### 3.6 Creating train, validation, and test files
### 3.7 Generating protein and SMILES embeddings
### 3.8 Training the ProSmith transformer model
### 3.9 Training the Gradient Boosting model
### 3.10 Mapping predictions back to the test set
### 3.11 Expected output files

## 4. No-leakage ProSmith workflow

### 4.1 Purpose of the no-leakage workflow
### 4.2 Reused steps from the standard ProSmith workflow
### 4.3 Required no-leakage files and folders
### 4.4 Expanding the no-leakage database
### 4.5 Creating the no-leakage train, validation, and test split
### 4.6 Checking the no-leakage split
### 4.7 Generating no-leakage embeddings
### 4.8 Training the no-leakage ProSmith transformer model
### 4.9 Training the no-leakage Gradient Boosting model
### 4.10 Saving no-leakage predictions
### 4.11 Mapping no-leakage predictions back to the test set
### 4.12 Expected output files

## 5. FusionESP predictor workflow

### 5.1 Purpose of the FusionESP predictor
### 5.2 Required FusionESP files and folders
### 5.3 Preparing FusionESP input data
### 5.4 Running the FusionESP predictor
### 5.5 Evaluating FusionESP prediction output
### 5.6 Expected output files

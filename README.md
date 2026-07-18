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
### 2.1 Prepare all files
Go to Kroll's GitHub repository:

https://github.com/AlexanderKroll/ProSmith

Download the dataset from Zenodo. 

#### 2.2 Working on the SURF supercomputer
Make sure you are in the correct directory. Then click the third icon in the left sidebar.

Under Clone a Repository, enter the URL of Kroll's GitHub repository. Upload the downloaded ZIP file into the ProSmith folder. 

Next, open a terminal and extract the dataset using: 

`unzip bestandsnaam.zip`

After extracting the archive, a folder named "data 2" will be created. Rename this folder to "data".

Your repository structure should now look approximately as follows:

```
├── code
├── data
├── LICENSE.md
└── README.md
```

### 2.3 Create a new notebook
From the launcher, navigate to:

Notebook -> Python 3 (ipykernel)

Copy the commands below into a notebook cel one at a time and execute each command before proceeding to the next one by clicking the "Run" button. 

`!wget https://github.com/mamba-org/micromamba-releases/releases/download/2.1.0-0/micromamba-linux-64`

`!chmod +x micromamba-linux-64`

`!mkdir -p ~/bin`

`!mv micromamba-linux-64 ~/bin/micromamba`

`!echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc`

`!source ~/.bashrc`

`!~/bin/micromamba --version`


### 2.4 Create the environment
Open a terminal and execuete the command below to create the Python environment for ProSmith. 

Run each command individually and wait for it to finish before executing the next one. 

`~/bin/micromamba env create -f environment.yml`

When prompted, type "Y" and then execute the following commands one by one: 

`eval "$(micromamba shell hook --shell bash)"`

`micromamba activate prosmith`

`pip install -r requirements.txt`

`micromamba install "mkl=2024.0" -c conda-forge`

`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

Whenever you start a new session on the SURF supercomputer, reactivate the environment using: 

`eval "$(micromamba shell hook --shell bash)"`

`micromamba activate prosmith`

## Kan dit weg pelo? (kopjes tot 3)
### 2.5 Creating or activating the environment
### 2.2 Installing dependencies
### 2.3 Navigating to the project repositories
### 2.4 Checking required datasets and model files
### 2.5 Testing the environment (you momma)

## 3. ProSmith workflow

### 3.1 Purpose
### 3.2 Required ProSmith files and folders

### 3.3 Standard ProSmith database workflow
#### 3.3.1 Preparing the original ProSmith database
#### 3.3.2 Creating train, validation, and test files
#### 3.3.3 Generating protein and SMILES embeddings
#### 3.3.4 Training the ProSmith transformer model
#### 3.3.5 Training the Gradient Boosting model
#### 3.3.6 Mapping predictions back to the test set
#### 3.3.7 Expected output files

### 3.4 Expanded ProSmith database workflow
#### 3.4.1 Expanding the ProSmith database
#### 3.4.2 Preprocessing the expanded database
#### 3.4.3 Creating train, validation, and test files
#### 3.4.4 Generating protein and SMILES embeddings
#### 3.4.5 Training the ProSmith transformer model
#### 3.4.6 Training the Gradient Boosting model
#### 3.4.7 Mapping predictions back to the test set
#### 3.4.8 Expected output files

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

# 5. FusionESP predictor workflow

## 5.1 Purpose of the FusionESP predictor

The FusionESP predictor is designed to predict enzyme–substrate interactions using the pretrained **FusionESP** model. The original FusionESP model was trained on datasets generated with the ProSmith framework developed by Alexander Kroll. This workflow enables users to perform predictions on custom peptide and substrate datasets without retraining the underlying model.

---

## 5.2 Required FusionESP files and folders

Before running the predictor, clone the original FusionESP repository:

```bash
git clone https://github.com/dzjxzyd/FusionESP.git
```

Navigate to the project directory:

```bash
cd FusionESP_server_1280
```

Activate the dedicated Python environment:

```bash
source fusionesp_env/bin/activate
```

If the environment has been activated successfully, the terminal prompt will display:

```bash
(fusionesp_env)
```

Start the FusionESP prediction server:

```bash
python app.py
```

After successful initialization, the following message should appear:

```text
* Running on http://127.0.0.1:5000
```

> **Important:** Keep this terminal open while performing predictions. Closing the server will interrupt the prediction process.

---

## 5.3 Preparing FusionESP input data

Create a directory for the prediction input files:

```bash
mkdir data_predictions
```

Place the input Excel file inside this directory.

The input file must meet the following requirements:

- The file must be in `.xlsx` format.
- Column names must match the input format required by FusionESP.
- Protein sequences and substrate SMILES should be formatted according to the original FusionESP specifications.

Example directory structure:

```text
data_predictions/
└── input_file.xlsx
```

---

## 5.4 Running the FusionESP predictor

Open a **new terminal** and activate the FusionESP environment again:

```bash
cd FusionESP_server_1280
source fusionesp_env/bin/activate
```

Execute the prediction using the following command.

Replace `input_file.xlsx` with the name of your input file.

```bash
curl -F "Peptide_sequences=@data_predictions/input_file.xlsx" \
http://127.0.0.1:5000/pred_with_file \
-o output_input_file/report_full.xlsx
```

Upon successful completion, FusionESP automatically generates an output directory containing the prediction results.

Example:

```text
output_input_file/
└── report_full.xlsx
```

---

## 5.5 Evaluating FusionESP prediction output

Prediction performance can be evaluated using several commonly applied binary classification metrics:

- Accuracy
- Precision
- Matthews Correlation Coefficient (MCC)
- Receiver Operating Characteristic Area Under the Curve (ROC-AUC)

The following script compares the FusionESP predictions with the ground-truth labels and calculates the corresponding evaluation metrics.

Replace `input_file` with the appropriate filename.

```bash
python -c "import pandas as pd, numpy as np; orig=pd.read_excel('data_predictions/input_file_sorted_longest_first.xlsx'); pred=pd.read_excel('output_input_file/report_full_sorted.xlsx'); df=pred.merge(orig[['Protein sequence','SMILES','output']], on=['Protein sequence','SMILES'], how='left'); df=df.dropna(subset=['output']); y_true=df['output'].astype(int).to_numpy(); pos_score=df.apply(lambda r: r['confidence_score'] if r['interaction']=='interaction' else 1-r['confidence_score'], axis=1).astype(float).to_numpy(); y_pred=(pos_score>0.5).astype(int); TP=((y_true==1)&(y_pred==1)).sum(); TN=((y_true==0)&(y_pred==0)).sum(); FP=((y_true==0)&(y_pred==1)).sum(); FN=((y_true==1)&(y_pred==0)).sum(); acc=(TP+TN)/len(y_true); prec=TP/(TP+FP) if TP+FP else float('nan'); mcc_d=((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))**0.5; mcc=((TP*TN)-(FP*FN))/mcc_d if mcc_d else float('nan'); ranks=pd.Series(pos_score).rank(method='average').to_numpy(); n_pos=(y_true==1).sum(); n_neg=(y_true==0).sum(); auc=(ranks[y_true==1].sum()-n_pos*(n_pos+1)/2)/(n_pos*n_neg) if n_pos and n_neg else float('nan'); print('N:', len(y_true)); print('TP TN FP FN:', TP, TN, FP, FN); print('Accuracy:', acc); print('Precision:', prec); print('MCC:', mcc); print('ROC-AUC:', auc)"
```

The script reports:

```text
N: Number of evaluated predictions
TP TN FP FN: Confusion matrix values
Accuracy
Precision
MCC
ROC-AUC
```

These metrics provide a quantitative assessment of the predictive performance of the FusionESP model on the supplied dataset.

---

## 5.6 Expected output files

After completing the workflow, the following files and folders should be available:

```text
FusionESP_server_1280/
├── data_predictions/
│   └── input_file.xlsx
│
├── output_input_file/
│   └── report_full.xlsx
```

The `report_full.xlsx` file contains the predicted interaction class together with the corresponding confidence score for each enzyme–substrate pair. This file serves as the primary output of the FusionESP prediction workflow.

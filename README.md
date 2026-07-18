# ProSmith_model_optimization_and_other_models
This repository was developed as part of PRJ61, a research project conducted within the Bachelor's programme in Chemistry at Hogeschool Rotterdam. The objective of the project was to investigate the application of artificial intelligence for enzyme-substrate interaction prediction by reproducing, optimizing, and extending the ProSmith workflow developed by Alexander Kroll. 

During the project, several workflows were implemented and evaluated, including the original ProSmith pipeline, and expanded database workflow, a no-leakage workflow, and the FusionESP predictor. These workflows were used to investigate the effects of datase expansion, data leakage prevention, and alternative prediction models on overall model performance. 

The workflows and scripts presented in this repository are the direct outcome of the PRJ61 project. They have been documented to enable reproducibility of the conducted experiments and to provide a practical guide for future users who wish to reproduce the results, extend the existing workflows, or apply the models to new datasets. 

Thank you for using this repository. We hope it contributes to your research and makes it easier to reproduce and build upon our work. 

Happy coding!

Aurelia, Pedro, and Zeynep

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

### 2.2 Working on the SURF supercomputer
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

## 3.4 Expanded ProSmith database workflow

### 3.4.1 Expanding the ProSmith database

To train ProSmith using an expanded enzyme–substrate database, several modifications to the original repository are required. These modifications enable the preprocessing and training pipeline to process the additional data correctly.

First, replace the original preprocessing script located at:

```text
code/preprocessing/preprocessing.py
```

with the provided `preprocessing_expandeddatabase.py` file.

Next, replace:

```text
code/training/utils/datautils.py
```

with `datautils_expandeddatabase.py`.

Finally, replace:

```text
code/training/training_GB.py
```

with `training_GB_expandeddatabase.py`.

After replacing each file, save the modifications before proceeding. Once these files have been updated, the ProSmith pipeline is configured to process the expanded enzyme–substrate database.


### 3.4.2 Preprocessing the expanded database

The original ProSmith datasets must be replaced by the expanded datasets before preprocessing can begin.

Navigate to:

```text
data/training_data/ESP/train_val
```

Rename the original datasets to preserve a backup:

```text
ESP_train_df.csv → ESP_train_df_old.csv
ESP_val_df.csv   → ESP_val_df_old.csv
ESP_test_df.csv  → ESP_test_df_old.csv
```

Next, copy the expanded datasets provided in this repository into the same directory.

#### Merging the training dataset

To retain all previously available training samples, the expanded training dataset should be merged with the original ProSmith training dataset.

This can be performed using spreadsheet software such as Microsoft Excel by appending the rows of the expanded dataset below the original training dataset.

Save the merged dataset as:

```text
ESP_train_df.csv
```

#### Converting the CSV format

The expanded datasets are distributed as semicolon-separated (`;`) CSV files, whereas the ProSmith pipeline expects comma-separated (`,`) CSV files.

Execute the following script to convert the datasets:

```bash
python - <<'PY'
...
PY
```

After the conversion has completed successfully, execute the cleaning script below to remove incomplete or invalid records:

```bash
python - <<'PY'
...
PY
```

This script performs several quality-control steps, including:

- Converting output labels to integer values.
- Removing rows containing missing labels.
- Removing incomplete protein or substrate entries.
- Removing rows with missing identifiers.
- Generating cleaned datasets for downstream processing.

After successful execution, the cleaned datasets are ready for embedding generation.


### 3.4.3 Creating train, validation, and test files

Before model training, embeddings must be generated for all protein sequences and SMILES strings present in the cleaned datasets.

Run the preprocessing pipeline using:

```bash
python code/preprocessing/preprocessing.py \
  --train_val_path data/training_data/ESP/train_val \
  --outpath data/training_data/ESP/embeddings \
  --smiles_emb_no 2000 \
  --prot_emb_no 2000
```

During preprocessing, the pipeline performs several automated operations:

- Validation of the input datasets.
- Preprocessing of protein sequences and SMILES strings.
- Generation of protein embeddings.
- Generation of molecular (SMILES) embeddings.
- Storage of all generated embeddings for subsequent model training.

Upon successful completion, newly generated embedding files will be available in:

```text
data/training_data/ESP/embeddings/
```

These embeddings serve as the input for both the ProSmith transformer model and the Gradient Boosting classifier.

### 3.4.4 Generating protein and SMILES embeddings

After the train, validation, and test datasets have been prepared, molecular and protein embeddings must be generated before model training can begin.

Execute the preprocessing pipeline using the following command:

```bash
python code/preprocessing/preprocessing.py \
  --train_val_path data/training_data/ESP/train_val \
  --outpath data/training_data/ESP/embeddings \
  --smiles_emb_no 2000 \
  --prot_emb_no 2000
```

The preprocessing pipeline automatically performs the following tasks:

- Reads the training and validation datasets.
- Generates transformer-based embeddings for all protein sequences.
- Generates ChemBERTa embeddings for all SMILES strings.
- Stores the generated embeddings for subsequent model training.

After successful execution, the generated embeddings can be found in:

```text
data/training_data/ESP/embeddings/
```

Before continuing with model training, it is recommended to verify that embeddings have been generated for all entries in the training and validation datasets.

To remove samples without corresponding embeddings, execute the following cleanup script:

```bash
python -u - <<'PY'
...
PY
```

This script compares the generated embeddings with the datasets and removes samples for which either the protein or SMILES embedding is unavailable. The resulting files are saved as:

```text
ESP_train_df_embedclean.csv
ESP_val_df_embedclean.csv
```

These cleaned datasets are subsequently used for model training.


### 3.4.5 Training the ProSmith transformer model

Once the embedding generation has been completed, the ProSmith transformer model can be trained using the expanded enzyme–substrate database.

Execute the following command:

```bash
python code/training/training.py \
  --train_dir data/training_data/ESP/train_val/ESP_train_df_embedclean.csv \
  --val_dir data/training_data/ESP/train_val/ESP_val_df_embedclean.csv \
  --save_model_path data/training_data/ESP/saved_model \
  --embed_path data/training_data/ESP/embeddings \
  --pretrained_model data/training_data/BindingDB/saved_model/pretraining_IC50_6gpus_bs144_1.5e-05_layers6.txt.pkl \
  --learning_rate 1e-5 \
  --num_hidden_layers 6 \
  --batch_size 24 \
  --binary_task True \
  --log_name ESP_embedclean \
  --num_train_epochs 100 \
  --port 29621 2>&1 | tee ESP_embedclean_training.log
```

Depending on the available computational resources, training may require several hours or multiple days.

The training process can be monitored using:

```bash
watch -n 2 nvidia-smi
```

to monitor GPU utilization, and

```bash
htop
```

to monitor CPU usage.

During training, ProSmith automatically generates log files that record the training progress and any potential errors. These logs are particularly useful when long-running training jobs are executed on the SURF supercomputer.

Upon completion, the trained transformer model is stored in:

```text
data/training_data/ESP/saved_model/
```


### 3.4.6 Training the Gradient Boosting model

Before training the Gradient Boosting classifier, the test dataset should be cleaned using the same embedding validation procedure that was applied to the training and validation datasets.

Execute the cleaning script:

```bash
python -u - <<'PY'
...
PY
```

This script removes test samples without valid protein or SMILES embeddings and creates an embedding-compatible test dataset.

Next, train the Gradient Boosting classifier using:

```bash
python -u code/training/training_GB.py \
  --train_dir data/training_data/ESP/train_val/ESP_train_df_embedclean.csv \
  --val_dir data/training_data/ESP/train_val/ESP_val_df_embedclean.csv \
  --test_dir data/training_data/ESP/train_val/ESP_test_df_embedclean.csv \
  --pretrained_model data/training_data/ESP/saved_model_rerun_100ep/best_model.pkl \
  --embed_path data/training_data/ESP/embeddings \
  --save_pred_path data/training_data/ESP/saved_predictions \
  --num_hidden_layers 6 \
  --num_iter 500 \
  --log_name ESP_GB_embedclean \
  --binary_task True 2>&1 | tee ESP_GB_embedclean.log
```

The Gradient Boosting classifier combines the learned transformer representations with the generated embeddings to improve predictive performance.

After successful completion, all prediction files are stored in:

```text
data/training_data/ESP/saved_predictions/
```


### 3.4.7 Mapping predictions back to the test set

The final step consists of mapping the generated predictions back to the original test dataset.

Execute the following script:

```bash
python - <<'PY'
...
PY
```

The script performs the following operations:

- Loads the predicted interaction scores.
- Retrieves the original test dataset.
- Maps each prediction to its corresponding sample.
- Creates a new dataset containing both the original data and the model predictions.

The resulting file is saved as:

```text
data/training_data/ESP/saved_predictions/ESP_test_with_predictions.csv
```

This file enables direct comparison between the original dataset and the predicted interaction labels.


### 3.4.8 Expected output files

After successfully completing the expanded database workflow, the repository should contain the following files and directories:

```text
data/
└── training_data/
    └── ESP/
        ├── embeddings/
        │   ├── Protein/
        │   └── SMILES/
        │
        ├── saved_model/
        │   └── best_model.pkl
        │
        ├── saved_predictions/
        │   ├── y_test_pred.npy
        │   ├── test_indices.npy
        │   └── ESP_test_with_predictions.csv
        │
        └── train_val/
            ├── ESP_train_df_embedclean.csv
            ├── ESP_val_df_embedclean.csv
            └── ESP_test_df_embedclean.csv
```

Successful generation of these files indicates that the expanded ProSmith workflow has been completed correctly and that the trained model and prediction outputs are available for downstream analysis and evaluation.

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

**Important:** Keep this terminal open while performing predictions. Closing the server will interrupt the prediction process.


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

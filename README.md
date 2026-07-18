# ProSmith_model_optimization_and_other_models
This repository was developed as part of PRJ61, a research project conducted within the Bachelor's programme in Chemistry at Hogeschool Rotterdam. The objective of the project was to investigate the application of artificial intelligence for enzyme-substrate interaction prediction by reproducing, optimizing, and extending the ProSmith workflow developed by Alexander Kroll. 

During the project, several workflows were implemented and evaluated, including the original ProSmith pipeline, and expanded database workflow, a no-leakage workflow, and the FusionESP predictor. These workflows were used to investigate the effects of datase expansion, data leakage prevention, and alternative prediction models on overall model performance. 

The workflows and scripts presented in this repository are the direct outcome of the PRJ61 project. They have been documented to enable reproducibility of the conducted experiments and to provide a practical guide for future users who wish to reproduce the results, extend the existing workflows, or apply the models to new datasets. 

Thank you for using this repository. We hope it contributes to your research and makes it easier to reproduce and build upon our work. 

Happy coding!

Aurelia, Pedro, and Zeynep

## Table of Contents

```
- Requirements
- 1. Project Overview
  - 1.1 Aim
  - 1.2 Included Models
  - 1.3 Repository Structure

- 2. Shared Environment Setup
  - 2.1 Prepare Files
  - 2.2 SURF Supercomputer
  - 2.3 Create Notebook
  - 2.4 Create Environment

- 3. ProSmith Workflow
  - 3.1 Purpose
  - 3.2 Required Files
  - 3.3 Baseline Workflow
    - 3.3.1 Create Datasets
    - 3.3.2 Generate Embeddings
    - 3.3.3 Train Transformer
    - 3.3.4 Train Gradient Boosting
    - 3.3.5 Map Predictions
    - 3.3.6 Expected Output
  - 3.4 Expanded Database Workflow
    - 3.4.1 Expand Database
    - 3.4.2 Preprocess Data
    - 3.4.3 Generate Embeddings
    - 3.4.4 Train Transformer
    - 3.4.5 Prepare Gradient Boosting
*For No-Leakage skip to Chapter 4*
    - 3.4.6 Train Gradient Boosting
    - 3.4.7 Map Predictions
    - 3.4.8 Expected Output

- 4. No-Leakage ProSmith Workflow
  - 4.1 Purpose
  - 4.2 Reused Steps
  - 4.3 Required Files
  - 4.4 Data Leakage Fix
    - 4.4.1 First Gradient Boosting Model
    - 4.4.2 Second Gradient Boosting Model
    - 4.4.3 Third Gradient Boosting Model
  - 4.5 Verify Changes
  - 4.6 Run Workflow
  - 4.7 Check Output
  - 4.8 Map Predictions
  - 4.9 Expected Output

- 5. FusionESP Workflow
  - 5.1 Purpose
  - 5.2 Setup
  - 5.3 Prepare Input
  - 5.4 Run Predictions
  - 5.5 Evaluate Results
  - 5.6 Expected Output

- Acknowledgements
```


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

This repository contains the combined reproducible workflow used for the ProSmith model optimization project. The repository brings together the shared environment setup, the standard ProSmith workflow, the no-leakage ProSmith workflow, and the FusionESP predictor workflow.

The goal of this repository is not to duplicate all individual project repositories in full, but to provide a clear and structured workflow that allows readers to reproduce the main steps used in this project.

### 1.1 Aim of this repository

The aim of this repository is to provide a summarized and reproducible workflow for setting up, modifying, and running the models used in this project.

This includes:

- setting up the shared ProSmith environment
- reproducing the standard ProSmith workflow
- applying the no-leakage modifications to the ProSmith workflow
- running the FusionESP predictor workflow
- generating the required output files for downstream analysis

The repository is intended to help readers understand how the different workflows were prepared and how the required files, scripts, and outputs are connected.

### 1.2 Models included in this repository

This repository contains workflows for the following models:

```text
Standard ProSmith workflow
No-leakage ProSmith workflow
FusionESP predictor workflow
```
The standard ProSmith workflow is used as the baseline workflow. 

The no-leakage ProSmith workflow is an adjusted version of the ProSmith workflow in which the training, validation, and test data are kept separated to prevent data leakage. 

The FusionESP predictor workflow is included as a separate prediction workflow.


### 1.3 Repository structure
```text
1. Project overview
2. Shared environment setup
3. Standard ProSmith database workflow
4. No-leakage ProSmith workflow
5. FusionESP predictor workflow
```

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

The purpose of this workflow is to reproduce the original ProSmith training pipeline as described by Kroll *et al.* using the original enzyme–substrate database. The workflow has been adapted for execution on the SURF supercomputer while preserving the original training procedure. Following this workflow enables users to reproduce the baseline ProSmith model, which serves as a reference for evaluating the optimized workflows presented in subsequent chapters.


### 3.2 Required ProSmith files and folders

Before starting the workflow, ensure that the following resources are available:

- The original ProSmith repository by Alexander Kroll.
- The corresponding dataset downloaded from Zenodo.
- A configured Python environment using Micromamba.
- Access to the SURF supercomputer.

Clone the original ProSmith repository and download the accompanying dataset before continuing with the workflow.


## 3.3 Standard ProSmith database workflow

After completing chapter 2, follow these steps

### 3.3.1 Creating train, validation, and test files

The original ProSmith repository already contains predefined training, validation, and test datasets.

No modifications to these datasets are required when reproducing the baseline model. Ensure that the following files are present:

```text
data/training_data/ESP/train_val/

├── ESP_train_df.csv
├── ESP_val_df.csv
└── ESP_test_df.csv
```

These datasets are used throughout the remainder of the baseline training workflow.


### 3.3.2 Generating protein and SMILES embeddings

Before training the ProSmith model, embeddings must be generated for all protein sequences and substrate SMILES strings contained in the training and validation datasets.

Execute the preprocessing pipeline:

```bash
python code/preprocessing/preprocessing.py \
  --train_val_path data/training_data/ESP/train_val \
  --outpath data/training_data/ESP/embeddings \
  --smiles_emb_no 2000 \
  --prot_emb_no 2000
```

The preprocessing pipeline performs the following tasks:

- Reads the training and validation datasets.
- Generates ESM-1b embeddings for all protein sequences.
- Generates ChemBERTa2 embeddings for all SMILES strings.
- Stores the generated embeddings in separate Protein and SMILES directories.

The generated embeddings are stored in:

```text
data/training_data/ESP/embeddings/
```

### 3.3.3 Training the ProSmith transformer model

Once all embeddings have been generated, the ProSmith transformer model can be trained using the original enzyme–substrate database.

Execute the following command:

```bash
python code/training/training.py \
    --train_dir data/training_data/ESP/train_val/ESP_train_df.csv \
    --val_dir data/training_data/ESP/train_val/ESP_val_df.csv \
    --save_model_path data/training_data/ESP/saved_model \
    --embed_path data/training_data/ESP/embeddings \
    --pretrained_model data/training_data/BindingDB/saved_model/pretraining_IC50_6gpus_bs144_1.5e-05_layers6.txt.pkl \
    --learning_rate 1e-5 \
    --num_hidden_layers 6 \
    --batch_size 24 \
    --binary_task True \
    --log_name ESP \
    --num_train_epochs 100
```

Depending on the available computational resources, training may require several hours. During training, model checkpoints and log files are automatically generated.

The trained model is saved in:

```text
data/training_data/ESP/saved_model/
```

### 3.3.4 Training the Gradient Boosting model

Following transformer training, train the Gradient Boosting classifier using the generated embeddings together with the transformer predictions.

Before executing the training script, modify the following line in `training_GB.py`:

```python
gpu = 0
```

Replace it with:

```python
gpu = device.index
```

Next, execute:

```bash
python code/training/training_GB.py \
    --train_dir data/training_data/ESP/train_val/ESP_train_df.csv \
    --val_dir data/training_data/ESP/train_val/ESP_val_df.csv \
    --test_dir data/training_data/ESP/train_val/ESP_test_df.csv \
    --pretrained_model data/training_data/ESP/saved_model/ESP_2gpus_bs48_1e-05_layers6.txt.pkl \
    --embed_path data/training_data/ESP/embeddings \
    --save_pred_path data/training_data/ESP/saved_predictions \
    --num_hidden_layers 6 \
    --num_iter 500 \
    --log_name ESP \
    --binary_task True
```

After successful execution, all prediction files are stored in:

```text
data/training_data/ESP/saved_predictions/
```

### 3.3.5 Mapping predictions back to the test set

The final step consists of mapping the generated predictions back to the original test dataset.

Execute the following script:

```bash
python - <<'PY'
import numpy as np
import pandas as pd
from os.path import join

pred_dir = "data/training_data/ESP/saved_predictions"
test_path = "data/training_data/ESP/train_val/ESP_test_df.csv"
out_path = join(pred_dir, "ESP_test_with_predictions.csv")

y_pred = np.load(join(pred_dir, "y_test_pred.npy"))
y_pred_ind = np.load(join(pred_dir, "test_indices.npy"))
test_df = pd.read_csv(test_path, sep=None, engine="python")

test_df["y_pred"] = np.nan
for k, ind in enumerate(y_pred_ind):
    test_df.loc[ind, "y_pred"] = y_pred[k]

test_df.to_csv(out_path, index=False)
print("Saved:", out_path)
print("Predictions mapped:", test_df["y_pred"].notna().sum())
print("Total rows:", len(test_df))
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

### 3.3.6 Expected output files

After successfully completing the baseline workflow, the repository should contain the following output:

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
            ├── ESP_train_df.csv
            ├── ESP_val_df.csv
            └── ESP_test_df.csv
```

Successful generation of these files indicates that the original ProSmith workflow has been completed successfully and that the baseline model is ready for downstream evaluation and comparison with the optimized workflows described in subsequent chapters.

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
import pandas as pd

files = [
    ("data/training_data/ESP/train_val/ESP_train_df.csv", "data/training_data/ESP/train_val/ESP_train_df_comma.csv"),
    ("data/training_data/ESP/train_val/ESP_val_df.csv", "data/training_data/ESP/train_val/ESP_val_df_comma.csv"),
]

for src, dst in files:
    df = pd.read_csv(src, sep=';')
    print(src, "->", dst)
    print(df.columns.tolist())
    df.to_csv(dst, index=False)
PY
```

After the conversion has completed successfully, execute the cleaning script below to remove incomplete or invalid records:

```bash
python - <<'PY'
import pandas as pd

pairs = [
    ("data/training_data/ESP/train_val/ESP_train_df_comma.csv",
     "data/training_data/ESP/train_val/ESP_train_df_clean.csv"),
    ("data/training_data/ESP/train_val/ESP_val_df_comma.csv",
     "data/training_data/ESP/train_val/ESP_val_df_clean.csv"),
]

for src, dst in pairs:
    df = pd.read_csv(src)
    df["output"] = pd.to_numeric(df["output"], errors="coerce")

    bad = df[df["output"].isna()]
    print("\n", src)
    print("Rows:", len(df))
    print("Bad output rows:", len(bad))
    if len(bad):
        print(bad[["Uniprot ID", "molecule ID", "output", "SMILES"]].head(20))

    df = df.dropna(subset=["output", "SMILES", "Protein sequence", "Uniprot ID", "molecule ID"])
    df["output"] = df["output"].astype(int)

    print("Clean rows:", len(df))
    print("Output values:", sorted(df["output"].unique()))
    df.to_csv(dst, index=False)
    print("Saved:", dst)
PY
```

This script performs several quality-control steps, including:

- Converting output labels to integer values.
- Removing rows containing missing labels.
- Removing incomplete protein or substrate entries.
- Removing rows with missing identifiers.
- Generating cleaned datasets for downstream processing.

After successful execution, the cleaned datasets are ready for embedding generation.


### 3.4.3 Generating protein and SMILES embeddings

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
import pickle as pkl
import torch
import pandas as pd
from pathlib import Path

embed_dir = Path("data/training_data/ESP/embeddings")

smiles = set()
smiles_files = sorted((embed_dir / "SMILES").glob("*"))
print("Loading SMILES files:", len(smiles_files), flush=True)

for f in smiles_files:
    print("Loading", f, flush=True)
    with open(f, "rb") as handle:
        d = pkl.load(handle)
    smiles.update(d.keys())
    print("  SMILES so far:", len(smiles), flush=True)

proteins = set()
protein_files = sorted((embed_dir / "Protein").glob("*.pt"))
print("Loading Protein files:", len(protein_files), flush=True)

for f in protein_files:
    print("Loading", f, flush=True)
    d = torch.load(f, map_location="cpu")
    proteins.update(d.keys())
    print("  Proteins so far:", len(proteins), flush=True)
    del d

print("SMILES embeddings:", len(smiles), flush=True)
print("Protein embeddings:", len(proteins), flush=True)

for src, dst in [
    ("data/training_data/ESP/train_val/ESP_train_df_clean.csv",
     "data/training_data/ESP/train_val/ESP_train_df_embedclean.csv"),
    ("data/training_data/ESP/train_val/ESP_val_df_clean.csv",
     "data/training_data/ESP/train_val/ESP_val_df_embedclean.csv"),
]:
    print("Filtering", src, flush=True)
    df = pd.read_csv(src)
    before = len(df)

    df["Protein sequence"] = df["Protein sequence"].astype(str).str[:1018]
    df = df[df["SMILES"].isin(smiles)]
    df = df[df["Protein sequence"].isin(proteins)]

    df.to_csv(dst, index=False)
    print(src, "->", dst, before, "to", len(df), flush=True)
PY
```

This script compares the generated embeddings with the datasets and removes samples for which either the protein or SMILES embedding is unavailable. The resulting files are saved as:

```text
ESP_train_df_embedclean.csv
ESP_val_df_embedclean.csv
```

These cleaned datasets are subsequently used for model training.


### 3.4.4 Training the ProSmith transformer model

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


### 3.4.5 Preparing for: Training the Gradient Boosting model

Before training the Gradient Boosting classifier, the test dataset should be cleaned using the same embedding validation procedure that was applied to the training and validation datasets.

Execute the cleaning script:

```bash
python -u - <<'PY'
import pickle as pkl
import torch
import pandas as pd
from pathlib import Path

test_src = "data/training_data/ESP/train_val/ESP_test_df.csv"
test_clean = "data/training_data/ESP/train_val/ESP_test_df_clean.csv"
test_embedclean = "data/training_data/ESP/train_val/ESP_test_df_embedclean.csv"
embed_dir = Path("data/training_data/ESP/embeddings")

# Read test CSV. Use sep=";" if the file is semicolon-separated.
try:
    df = pd.read_csv(test_src)
    if len(df.columns) == 1 and ";" in df.columns[0]:
        df = pd.read_csv(test_src, sep=";")
except Exception:
    df = pd.read_csv(test_src, sep=";")

df["output"] = pd.to_numeric(df["output"], errors="coerce")
before = len(df)

df = df.dropna(subset=["output", "SMILES", "Protein sequence", "Uniprot ID", "molecule ID"])
df["output"] = df["output"].astype(int)
df.to_csv(test_clean, index=False)

print("Clean:", test_src, "->", test_clean, before, "to", len(df), flush=True)

smiles = set()
for f in sorted((embed_dir / "SMILES").glob("*")):
    with open(f, "rb") as handle:
        smiles.update(pkl.load(handle).keys())

proteins = set()
for f in sorted((embed_dir / "Protein").glob("*.pt")):
    d = torch.load(f, map_location="cpu")
    proteins.update(d.keys())
    del d

before_embed = len(df)
df["Protein sequence"] = df["Protein sequence"].astype(str).str[:1018]
df = df[df["SMILES"].isin(smiles)]
df = df[df["Protein sequence"].isin(proteins)]
df.to_csv(test_embedclean, index=False)

print("Embedclean:", test_clean, "->", test_embedclean, before_embed, "to", len(df), flush=True)
print("Saved:", test_embedclean, flush=True)
PY
```

This script removes test samples without valid protein or SMILES embeddings and creates an embedding-compatible test dataset.

## *Next Steps*
The ProSmith model has now been successfully trained using the reproduced baseline pipeline. The next step is to improve the predictive performance by training the Gradient boosting ensemble using the generated embeddings and model predictions. This procedure is discribed in the following section and reproduces the original ProSmith workflow, including the originial data splitting strategy. 

After completing the training in step 3.4.5, you can continue with Chapter 4, where the entire pipeline is repeated using a leakage-free gradient boosting to obtain a more robust and unbiased evaluation of the model.

### 3.4.6 Preparing for: Training the Gradient Boosting model

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
import numpy as np
import pandas as pd
from os.path import join

pred_dir = "data/training_data/ESP/saved_predictions"
test_path = "data/training_data/ESP/train_val/ESP_test_df.csv"
out_path = join(pred_dir, "ESP_test_with_predictions.csv")

y_pred = np.load(join(pred_dir, "y_test_pred.npy"))
y_pred_ind = np.load(join(pred_dir, "test_indices.npy"))
test_df = pd.read_csv(test_path, sep=None, engine="python")

test_df["y_pred"] = np.nan
for k, ind in enumerate(y_pred_ind):
    test_df.loc[ind, "y_pred"] = y_pred[k]

test_df.to_csv(out_path, index=False)
print("Saved:", out_path)
print("Predictions mapped:", test_df["y_pred"].notna().sum())
print("Total rows:", len(test_df))
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
The purpose of the no-leakage workflow is to create an optimized ProSmith workflow in which data leakage between the training, validation, and test sets is prevented. In this workflow, the model is trained, validated, and tested using separately prepared datasets, so that the final test set remains independent from the data used during model development.

This workflow was included because overlap between enzyme–substrate combinations across different data splits can lead to an overestimation of model performance. By keeping the train, validation, and test sets separated throughout the workflow, the final predictions give a more reliable indication of how the model performs on unseen enzyme–substrate combinations.

The no-leakage workflow follows the same general ProSmith training structure as the standard workflow, but uses adjusted data handling, a no-leakage database split, and separate output files for the leakage-free setup.

### 4.2 Reused steps from the standard ProSmith workflow
```text
The following steps are reused from the standard ProSmith workflow:

- using the same ProSmith environment
- preparing input files in the required ProSmith format
- generating protein and SMILES embeddings
- training the ProSmith transformer model

The main difference is that the no-leakage workflow uses an alternate code that prevents model overestimation and keeps the datasets separate.
```

### 4.3 Required no-leakage files and folders
```text
training.py
training_GB.py
Gradient_Boost_No_Leakage.zip
```
Gradient_Boost_No_Leakage.zip contains the no-leakage gradient boosting splits including the ensemble-weights. These files replace the standard ProSmith gradient boosting outputs. 

Training.py file is used to train the no-leakge ProSmith transformer model. The training_GB.py file is used to train the no-leakage gradient boosting model.

### 4.4 Applying the data leakage fix in `training_GB.py`

The main no-leakage modification is applied in `training_GB.py`. In the original Gradient Boosting workflow, the validation set was partly reused when training the final Gradient Boosting models that were evaluated on the test set. 

This is not desired, because the validation set should only be used for model selection and should not become part of the final training data used for test-set predictions.

In the no-leakage workflow, the validation set is only used for:

- hyperparameter selection
- ensemble weight selection

The validation set is not added back into the training data when generating the final predictions on the test set.

Open the following file:

```text
training_GB.py
```
#### 4.4.1 Modify the first Gradient Boosting model
Find the following code:
```bash
bst_all_test, y_test_pred_all = get_predictions(
    param = trials.argmin,
    dM_train = dtrain_val,
    dM_val = dtest
)
```
Replace it with:
```bash
bst_all_test, y_test_pred_all = get_predictions(
    param = trials.argmin,
    dM_train = dtrain,
    dM_val = dtest
)
```
This prevents the combined train-validation matrix from being used for the final test-set prediction step.

#### 4.4.1 Modify the second Gradient Boosting model
Find the following code:
```bash
bst_all_cls_test, y_test_pred_all_cls = get_predictions(
    param = trials.argmin,
    dM_train = dtrain_val_all_cls,
    dM_val = dtest_all_cls
)
```
Replace it with:
```bash
bst_all_cls_test, y_test_pred_all_cls = get_predictions(
    param = trials.argmin,
    dM_train = dtrain_all_cls,
    dM_val = dtest_all_cls
)
```
This applies the same no-leakage correction to the Gradient Boosting model that uses the ESM1b, ChemBERTa2, and cls-token features.

#### 4.4.3 Modify the third Gradient Boosting model
Find the following code:
```bash
bst_cls_test, y_test_pred_cls = get_predictions(
    param = trials.argmin,
    dM_train = dtrain_val_cls,
    dM_val = dtest_cls
)
```
Replace it with:
```bash
bst_cls_test, y_test_pred_cls = get_predictions(
    param = trials.argmin,
    dM_train = dtrain_cls,
    dM_val = dtest_cls
)
```
This applies the no-leakage correction to the cls-token-only Gradient Boosting model.

### 4.5 Checking that the no-leakage correction is applied correctly
After editing `training_GB.py`, check that the old train-validation objects are no longer used for the final test-set predictions.

The following objects may still exist in the script:

```text
dtrain_val
dtrain_val_all_cls
dtrain_val_cls
```
However, these objects should not be used when generating the final test-set predictions for:
```text
bst_all_test
bst_all_cls_test
bst_cls_test
```
The final test-set predictions should use only the training-data objects:
```text
dtrain
dtrain_all_cls
dtrain_cls
```
This ensures that the validation set remains separate from the final model training step used for test-set prediction.

### 4.6 Running the no-leakage Gradient Boosting workflow
After applying the no-leakage correction, run the Gradient Boosting workflow using separate output folders. 

This prevents the original and no-leakage results from being mixed.
```bash
python code/training/training_GB.py \
    --train_dir data/training_data/ESP/train_val/ESP_train_df.csv \
    --val_dir data/training_data/ESP/train_val/ESP_val_df.csv \
    --test_dir data/training_data/ESP/train_val/ESP_test_df.csv \
    --pretrained_model data/training_data/ESP/saved_model/ESP_2gpus_bs48_1e-05_layers6.txt.pkl \
    --embed_path data/training_data/ESP/embeddings \
    --save_pred_path data/training_data/ESP/saved_predictions_no_leakage \
    --save_gb_model_path data/training_data/ESP/saved_gb_model_no_leakage \
    --num_hidden_layers 6 \
    --num_iter 500 \
    --log_name ESP_no_leakage \
    --binary_task True
```
The important difference from the standard workflow is that the no-leakage output is saved in separate folders:
```text
saved_predictions_no_leakage
saved_gb_model_no_leakage
```
### 4.7 Checking the no-leakage output files
After running the no-leakage Gradient Boosting workflow, check whether the no-leakage Gradient Boosting models were saved correctly.

Run:
```bash
ls data/training_data/ESP/saved_gb_model_no_leakage/
```
The expected output is:
```text
gb_all.json
gb_all_cls.json
gb_cls.json
ensemble_weights.json
```
Next, check whether the no-leakage prediction files were saved:
```bash
ls data/training_data/ESP/saved_predictions_no_leakage/
```
The expected output is:
```text
y_test_pred.npy
test_indices.npy
```
The y_test_pred.npy file contains the predicted scores for the test set. 

The test_indices.npy file contains the row indices needed to link the predictions back to the correct test-set entries.

### 4.8 Mapping no-leakage predictions back to the test set
After running the no-leakage Gradient Boosting workflow, the predictions are stored separately from the original test set. 

To make the output easier to interpret, the predictions should be mapped back to the corresponding rows in the test file.

Run the following code in a Jupyter Notebook or Python script:

```python
import numpy as np
import pandas as pd
from os.path import join

pred_dir = "data/training_data/ESP/saved_predictions_no_leakage"
test_path = "data/training_data/ESP/train_val/ESP_test_df.csv"
out_path = join(pred_dir, "ESP_test_with_predictions.csv")

y_pred = np.load(
    join(
        pred_dir,
        "y_test_pred.npy"
    )
)

y_pred_ind = np.load(
    join(
        pred_dir,
        "test_indices.npy"
    )
)

test_df = pd.read_csv(
    test_path
)

test_df["y_pred"] = np.nan

for k, ind in enumerate(y_pred_ind):
    test_df.loc[int(ind), "y_pred"] = y_pred[k]

test_df.to_csv(
    out_path,
    index=False
)

print("Saved:", out_path)
print("Predictions mapped:", test_df["y_pred"].notna().sum())
print("Total rows:", len(test_df))
```
This creates the final mapped prediction file:
```text
ESP_test_with_predictions.csv
```
This file contains the original no-leakage test-set information together with the predicted model scores.

### 4.9 Expected output files
After completing the no-leakage workflow, the following output files should be present:
```text
gb_all.json
gb_all_cls.json
gb_cls.json
ensemble_weights.json
y_test_pred.npy
test_indices.npy
ESP_test_with_predictions.csv
```

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

# Acknowledgement
We would like to express our sincere gratitude to Max Achterweust for his guidance, support, and expertise throughout this project. 

From introducing us to the ProSmith workflow to helping us navigate Python, machine learning, and the SURF supercomputer, your knowledge and willingness to answer our many questions have been invaluable. Your support enabled us not only to succesfully reproduce the original ProSmith pipeline, but also to extend and improve it by training new models with an expanded enzym-substrate database. Whenever we encountered technical challenges, your patience and enthusiasm helped us move forward. 

This prject has provided us with invaluable experience at the intersection of artificial intelligence and biochemistry, while also giving us the opporunity to contribute to ongoing research. It has been a pleasure working with you, and we are truly grateful for the time, encouragement, and dedication you invested in our group. Thank you for making this project such an enjoyable, educational, and rewarding experience!


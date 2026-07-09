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

# Kan dit weg pelo?
### 2.5 Creating or activating the environment
### 2.2 Installing dependencies
### 2.3 Navigating to the project repositories
### 2.4 Checking required datasets and model files
### 2.5 Testing the environment (you momma)

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

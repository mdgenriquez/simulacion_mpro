import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from stmol import showmol
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from padelpy import from_smiles
# from PaDEL_pywrapper import PaDEL
# from PaDEL_pywrapper import descriptors
import numpy as np
import pickle
import joblib

st.title("Test de Mpro para ligando-receptor")

compound_smiles=st.text_input('Ingresa tu código SMILES','C1=CC(=CC=C1C2C(C(=O)C3=C(C=C(C=C3O2)O)O)O)O')
mm = Chem.MolFromSmiles(compound_smiles)

Draw.MolToFile(mm,'mol.png')
st.image('mol.png')

#archivos
RDKit_select_descriptors = joblib.load('./archivos/RDKit_select_descriptors.pickle')

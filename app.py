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

st.title("Test de Mpro para ligando-proteina")

compound_smiles=st.text_input('Ingresa tu código SMILES','C1=CC(=CC=C1C2C(C(=O)C3=C(C=C(C=C3O2)O)O)O)O')
mm = Chem.MolFromSmiles(compound_smiles)

Draw.MolToFile(mm,'mol.png')
st.image('mol.png')

#archivos
RDKit_select_descriptors = joblib.load('archivos/RDKit_select_descriptors.pickle')
PaDEL_select_descriptors = joblib.load('archivos/PaDEL_select_descriptors.pickle')
robust_scaler = joblib.load('archivos/robust_scaler.pickle')
minmax_scaler = joblib.load('archivos/minmax_scaler.pickle')
nusvr_best = joblib.load('archivos/nusvr_best_model.pickle')
krr_best = joblib.load('archivos/krr_best_model.pickle')
hgb_best = joblib.load('archivos/hgb_best_model.pickle')
selector_ExtraTrees = joblib.load('archivos/selector_ExtraTrees.pickle')
selector_Huber = joblib.load('archivos/selector_Huber.pickle')
selector_LGBM = joblib.load('archivos/selector_LGBM.pickle')
svr_best_model = joblib.load('archivos/svr_best_model.pickle')

# RDKit selected descriptors function
def get_selected_RDKitdescriptors(smile, selected_descriptors, missingVal=None):
    ''' Calculates only the selected descriptors for a molecule '''
    res = {}
    mol = Chem.MolFromSmiles(smile)
    if mol is None:
        return {desc: missingVal for desc in selected_descriptors}

    for nm, fn in Descriptors._descList:
        if nm in selected_descriptors:
            try:
                res[nm] = fn(mol)
            except:
                import traceback
                traceback.print_exc()
                res[nm] = missingVal
    return res

df = pd.DataFrame({'smiles': [compound_smiles]})
#st.dataframe(df)

# Calculate selected RDKit descriptors
RDKit_descriptors = [get_selected_RDKitdescriptors(m, RDKit_select_descriptors) for m in df['smiles']]
RDKit_df = pd.DataFrame(RDKit_descriptors)
st.write("Descriptores RDKit")
st.dataframe(RDKit_df)

# Calculate PaDEL descriptors
PaDEL_descriptors = from_smiles(df['smiles'].tolist())
PaDEL_df_ = pd.DataFrame(PaDEL_descriptors)
PaDEL_df = PaDEL_df_.loc[:,PaDEL_select_descriptors]
st.write("Descriptores PaDEL")
st.dataframe(PaDEL_df)

# Concatenate RDKit and PaDEL dataframes
RDKit_PaDEL_df = pd.concat([RDKit_df, PaDEL_df], axis=1)
RDKit_PaDEL_df_columns = RDKit_PaDEL_df.columns

# Scale data---consultar sobre los otros archivos
RDKit_PaDEL_scaled_ = robust_scaler.transform(RDKit_PaDEL_df)
RDKit_PaDEL_scaled = minmax_scaler.transform(RDKit_PaDEL_scaled_)
RDKit_PaDEL_scaled_df = pd.DataFrame(RDKit_PaDEL_scaled)
RDKit_PaDEL_scaled_df.columns = RDKit_PaDEL_df_columns

# Selected features
selected_features_mask = selector_LGBM.support_
Selected_features = RDKit_PaDEL_df_columns[selected_features_mask]
RDKit_PaDEL = RDKit_PaDEL_scaled_df[Selected_features]
# Cargar el modelo (elige uno disponible en tu repo)
svr_best_model = joblib.load('archivos/svr_best_model.pickle')  

# Mostrar la predicción en Streamlit
st.write("Free Energy Binding Prediction")
st.dataframe(pd.DataFrame(predictions, columns=["Docking Score"]))  # Convertir a DataFrame





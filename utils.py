# -*- coding: utf-8 -*-

"""Helper functions"""

import math
import pandas as pd

# from tqdm import tqdm
# import pubchempy
from py2neo import Graph
from rdkit.Chem import CanonSmiles

# from pubchempy import get_compounds

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Neo4J Server
FRAUNHOFER_ADMIN_NAME = "neo4j"
FRAUNHOFER_ADMIN_PASS = "remedi4all-2023"
FRAUNHOFER_URL = "neo4j+s://f43b07b7.databases.neo4j.io:7687"


def connect_to_kg():
    graph = Graph(
        FRAUNHOFER_URL,
        auth=(FRAUNHOFER_ADMIN_NAME, FRAUNHOFER_ADMIN_PASS),
    )
    return graph


def check_smile(smile: str):
    """Method to check if SMILES is valid."""
    try:
        CanonSmiles(smile)
        return True
    except ValueError:
        return False


def get_idx_from_smile(smiles: str):
    """Method to get pubchem and chembl compound id from SMILES."""

    if pd.isna(smiles):
        return None, None, None

    if not check_smile(smiles):
        return None, None, None

    try:
        compounds = get_compounds(smiles, "smiles")
    except pubchempy.BadRequestError:
        print(smiles)
        return None, None, None

    if len(compounds) < 1:
        return None, None, None

    compound = compounds[0]

    if not compound.synonyms:
        return None, None, compound.cid

    name = compound.synonyms[0]
    for idx in compound.synonyms:
        if idx.startswith("CHEMBL"):
            return name, idx, compound.cid

    return name, None, compound.cid


def val_to_pchembl(val: str, unit: str):
    """Converting original values to pChEMBL values."""
    if pd.isna(val) or val == "0.0":
        return 0
    elif unit == "nM" and pd.notna(val):
        return round(9 - math.log10(float(val)))
    elif unit == "uM" and pd.notna(val):
        return round(6 - math.log10(float(val)))
    elif unit == "mM" and pd.notna(val):
        return round(3 - math.log10(float(val)))
    else:
        return 0


def pchembl_to_val(val: str, unit: str):
    """Converting pChEMBL values to original values."""
    if unit == "M":
        return 10 ** (0 - float(val))
    elif unit == "nM":
        return 10 ** (9 - float(val))
    elif unit == "uM":
        return 10 ** (6 - float(val))
    elif unit == "mM":
        return 10 ** (3 - float(val))
    else:
        raise ValueError(f"Unknown unit {unit}")


def pchembls_to_val(value_df: pd.Series, unit: str):
    """Converting pCHeMBL series to original values."""

    values = []
    for val in tqdm(value_df, desc="Converting pChEMBL to original values"):
        values.append(pchembl_to_val(val, unit))

    return values

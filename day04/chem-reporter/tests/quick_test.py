# test of connection internal of the project
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.config import settings
from src.models import Result, MeltingPoint

print("Settings:", settings)
r = Result(input_smiles="CC(=O)OC1=CC=CC=C1C(=O)O")  # aspirin
print("Result OK, fields:", r.to_dict().keys())

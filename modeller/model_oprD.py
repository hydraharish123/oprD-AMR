from modeller import *
from modeller.automodel import *

env = Environ()

env.io.atom_files_directory = ['../structures']
env.io.hetatm = False

# 1. ADD CRITICAL ARGUMENT: Tell AutoModel to calculate the DOPE score
a = AutoModel(
    env,
    alnfile='OprD_WT.ali',
    knowns='3SY7',
    sequence='OprD_WT',
    assess_methods=(assess.DOPE,)  # <-- MUST INCLUDE THIS
)

a.starting_model = 1
a.ending_model = 10

a.make()

print("\nMODEL RESULTS")
print("=" * 70)

for model in a.outputs:
    # Skip models that failed to build completely
    if model['failure'] is not None:
        continue
        
    filename = model['name']
    molpdf = model['molpdf']
    
    # 2. SUCCESS: This key will now exist in the dictionary
    dope_score = model['DOPE score']

    print(
        f"{filename:30s} "
        f"molpdf = {molpdf:10.3f} "
        f"DOPE = {dope_score:12.3f}"
    )

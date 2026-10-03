from Bio.PDB import PDBParser

pdb_file = "../structures/3SY7.pdb"

parser = PDBParser(QUIET=True)
structure = parser.get_structure("3SY7", pdb_file)
chain = structure[0]["A"]

# ---------------------------------------------------------
# 1. Extract residues that actually have coordinates
#    from native OprD PDB residues 1–420.
# ---------------------------------------------------------

aa_map = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D",
    "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
    "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
    "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
}

coord_residues = {}

for residue in chain:
    if residue.id[0] == " ":
        pdb_num = residue.id[1]

        if 1 <= pdb_num <= 420:
            coord_residues[pdb_num] = aa_map[residue.resname]


# ---------------------------------------------------------
# 2. Construct the template sequence according to
#    PDB numbering.
#
#    Missing crystal residues become '-'.
# ---------------------------------------------------------

template = ""

for i in range(1, 421):
    template += coord_residues.get(i, "-")


# ---------------------------------------------------------
# 3. Canonical mature OprD sequence.
#
#    UniProt P32722
#    Remove residues 1–23 (signal peptide).
# ---------------------------------------------------------

uniprot = (
    "MKVMKWSAIALAVSAGSTQFAVADAFVSDQAEAKGFIEDSSLDLLLRNYYFNRDGKSGSGDRVDWTQGFL"
    "TTYESGFTQGTVGFGVDAFGYLGLKLDGTSDKTGTGNLPVMNDGKPRDDYSRAGGAVKVRISKTMLKWGEM"
    "QPTAPVFAAGGSRLFPQTATGFQLQSSEFEGLDLEAGHFTEGKEPTTVKSRGELYATYAGETAKSADFIGG"
    "RYAITDNLSASLYGAELEDIYRQYYLNSNYTIPLASDQSLGFDFNIYRTNDEGKAKAGDISNTTWSLAAAY"
    "TLDAHTFTLAYQKVHGDQPFDYIGFGRNGSGAGGDSIFLANSVQYSDFNGPGEKSWQARYDLNLASYGVPGL"
    "TFMVRYINGKDIDGTKMSDNNVGYKNYGYGEDGKHHETNLEAKYVVQSGPAKDLSFRIRQAWHRANADQGEG"
    "DQNEFRLIVDYPLSIL"
)

# First 23 residues = signal peptide
target = uniprot[23:]


# ---------------------------------------------------------
# 4. Check lengths
# ---------------------------------------------------------

print("Full UniProt length:", len(uniprot))
print("Mature target length:", len(target))
print("Template length:", len(template))

print("\nTemplate:")
print(template)

print("\nTarget:")
print(target)


# ---------------------------------------------------------
# 5. Write MODELLER alignment
# ---------------------------------------------------------

with open("OprD_WT.ali", "w") as f:

    f.write(">P1;3SY7\n")
    f.write("structureX:3SY7:1:A:420:A:::-1.00:-1.00\n")
    f.write(template)
    f.write("*\n\n")

    f.write(">P1;OprD_WT\n")
    f.write("sequence:OprD_WT::::::::\n")
    f.write(target)
    f.write("*\n")

print("\nAlignment written to OprD_WT.ali")
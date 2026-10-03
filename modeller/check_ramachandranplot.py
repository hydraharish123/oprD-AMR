from Bio.PDB import PDBParser, PPBuilder
import matplotlib.pyplot as plt

pdb_file = "OprD_WT.B99990004.pdb"

parser = PDBParser(QUIET=True)
structure = parser.get_structure("OprD", pdb_file)

model = structure[0]
chain = model["A"]

ppb = PPBuilder()

phis = []
psis = []
residue_numbers = []
residue_names = []

for poly in ppb.build_peptides(chain):

    for residue, (phi, psi) in zip(poly, poly.get_phi_psi_list()):

        if phi is not None and psi is not None:

            phis.append(phi * 180.0 / 3.14159265359)
            psis.append(psi * 180.0 / 3.14159265359)

            residue_numbers.append(residue.id[1])
            residue_names.append(residue.resname)


# ---------------------------------------------------------
# Print residues in the four MODELLER-built regions
# ---------------------------------------------------------

modeled_regions = [
    (32, 37),
    (77, 94),
    (160, 170),
    (287, 290)
]

print("\nMODELED-REGION BACKBONE ANGLES")
print("=" * 60)

for num, name, phi, psi in zip(
    residue_numbers, residue_names, phis, psis
):

    for start, end in modeled_regions:

        if start <= num <= end:

            print(
                f"{num:4d} {name:3s} "
                f"phi = {phi:8.2f} "
                f"psi = {psi:8.2f}"
            )


# ---------------------------------------------------------
# Plot Ramachandran map
# ---------------------------------------------------------

plt.figure(figsize=(7, 7))

plt.scatter(phis, psis, s=15)

plt.xlim(-180, 180)
plt.ylim(-180, 180)

plt.xlabel("Phi (°)")
plt.ylabel("Psi (°)")
plt.title("OprD WT — Ramachandran Plot")

plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)

plt.grid(alpha=0.2)

plt.show()
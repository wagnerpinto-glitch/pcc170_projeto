from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = Path("/home/wagner/pcc170/csv/ai_student_impact_dataset.csv")
df = pd.read_csv(csv_path)

df["Delta_GPA"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]
PASSIVE_USE_CASES = {"Copywriting/Drafting", "Direct_Answer_Generation"}
df["A"] = np.where(df["Primary_Use_Case"].isin(PASSIVE_USE_CASES), 1, -1)
stem_junior = df.loc[
    (df["Major_Category"] == "STEM") & (df["Year_of_Study"] == "Junior")
].copy()

ANXIETY_Q2 = stem_junior["Anxiety_Level_During_Exams"].median()
STUDY_Q2 = stem_junior["Traditional_Study_Hours"].median()
stem_junior["B"] = np.where(
    stem_junior["Anxiety_Level_During_Exams"] > ANXIETY_Q2, 1, -1
)
stem_junior["C"] = np.where(
    stem_junior["Traditional_Study_Hours"] > STUDY_Q2, 1, -1
)
factorial = stem_junior.copy()

CELLS = [
    (a, b, c)
    for c in (-1, 1)
    for b in (-1, 1)
    for a in (-1, 1)
]
groups = {
    key: frame["Delta_GPA"].to_numpy()
    for key, frame in factorial.groupby(["A", "B", "C"], sort=False)
}
cell_means = {cell: groups[cell].mean() for cell in CELLS}

def equal_cell_mean(fixed_levels):
    selected = [
        cell_means[cell]
        for cell in CELLS
        if all(cell[index] == level for index, level in fixed_levels.items())
    ]
    return float(np.mean(selected))

# Teste Fator A
mA_neg = equal_cell_mean({0: -1})
mA_pos = equal_cell_mean({0: 1})
print(f"Fator A: neg={mA_neg:.4f}, pos={mA_pos:.4f}")

# Teste Fator B
mB_neg = equal_cell_mean({1: -1})
mB_pos = equal_cell_mean({1: 1})
print(f"Fator B: neg={mB_neg:.4f}, pos={mB_pos:.4f}")

# Teste Fator C
mC_neg = equal_cell_mean({2: -1})
mC_pos = equal_cell_mean({2: 1})
print(f"Fator C: neg={mC_neg:.4f}, pos={mC_pos:.4f}")

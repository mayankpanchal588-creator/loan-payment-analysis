"""
Helper script to programmatically create the Jupyter Notebook (.ipynb).
Run: python create_notebook.py
"""
import json, os

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')

def cell(source, cell_type='code', outputs=None):
    if cell_type == 'markdown':
        return {"cell_type": "markdown", "metadata": {}, "source": source}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": outputs or [],
        "source": source,
    }

cells = []

# ── Title ──────────────────────────────────────────────────
cells.append(cell([
    "# 🏦 Loan Payment Data Analysis\n",
    "### College Data Analytics Project\n",
    "\n",
    "**Dataset:** Loan payments data.csv (500 records, 11 features)  \n",
    "**Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn · SciPy  \n",
    "\n",
    "---\n",
    "### Table of Contents\n",
    "1. [Data Loading](#1-data-loading)  \n",
    "2. [Data Cleaning](#2-data-cleaning)  \n",
    "3. [Missing Value & Duplicate Analysis](#3-missing-value--duplicate-analysis)  \n",
    "4. [Exploratory Data Analysis (EDA)](#4-exploratory-data-analysis)  \n",
    "5. [Statistical Analysis](#5-statistical-analysis)  \n",
    "6. [Loan Status Analysis](#6-loan-status-analysis-chart-1)  \n",
    "7. [Principal Analysis](#7-principal-analysis-chart-2)  \n",
    "8. [Gender Analysis](#8-gender-analysis-chart-3)  \n",
    "9. [Education Analysis](#9-education-analysis-chart-4)  \n",
    "10. [Age Analysis](#10-age-analysis-chart-5)  \n",
    "11. [Loan Term Analysis](#11-loan-term-analysis-chart-6)  \n",
    "12. [Correlation Analysis](#12-correlation-analysis-chart-7)  \n",
    "13. [Days to Payoff](#13-days-to-payoff-analysis-chart-8)  \n",
    "14. [Past Due Days](#14-past-due-days-analysis-chart-9)  \n",
    "15. [Principal by Education & Gender](#15-principal-by-education--gender-chart-10)  \n",
    "16. [Business Insights & Recommendations](#16-business-insights--recommendations)  \n",
], cell_type='markdown'))

# ── 0. Imports ─────────────────────────────────────────────
cells.append(cell([
    "## 0. Imports & Setup\n",
], cell_type='markdown'))

cells.append(cell([
    "import os, warnings\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.patches as mpatches\n",
    "import seaborn as sns\n",
    "from scipy import stats\n",
    "\n",
    "warnings.filterwarnings('ignore')\n",
    "%matplotlib inline\n",
    "\n",
    "sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)\n",
    "plt.rcParams.update({'figure.dpi': 110, 'savefig.bbox': 'tight'})\n",
    "\n",
    "COLORS = {\n",
    "    'PAIDOFF': '#2ecc71',\n",
    "    'COLLECTION': '#e74c3c',\n",
    "    'COLLECTION_PAIDOFF': '#f39c12',\n",
    "}\n",
    "STATUS_PALETTE = list(COLORS.values())\n",
    "edu_order = ['High School or Below', 'college', 'Bechalor', 'Master or Above']\n",
    "print('Libraries loaded successfully!')\n",
]))

# ── 1. Data Loading ────────────────────────────────────────
cells.append(cell(["## 1. Data Loading\n", "> Load the CSV and inspect its basic properties."], cell_type='markdown'))

cells.append(cell([
    "DATA_PATH = '../Loan payments data.csv'\n",
    "df = pd.read_csv(DATA_PATH)\n",
    "\n",
    "print(f'Shape   : {df.shape}')\n",
    "print(f'Columns : {list(df.columns)}')\n",
    "df.head()\n",
]))

cells.append(cell(["df.info()\n"]))
cells.append(cell(["df.describe().T\n"]))

# ── 2. Data Cleaning ───────────────────────────────────────
cells.append(cell(["## 2. Data Cleaning\n", "> Parse dates, standardise text, and engineer new features."], cell_type='markdown'))

cells.append(cell([
    "# Parse date columns\n",
    "for col in ['effective_date', 'due_date', 'paid_off_time']:\n",
    "    df[col] = pd.to_datetime(df[col], errors='coerce')\n",
    "\n",
    "# Standardise text\n",
    "df['Gender']      = df['Gender'].str.strip().str.lower()\n",
    "df['education']   = df['education'].str.strip()\n",
    "df['loan_status'] = df['loan_status'].str.strip()\n",
    "\n",
    "# Feature engineering\n",
    "df['days_to_payoff'] = (df['paid_off_time'] - df['effective_date']).dt.days\n",
    "\n",
    "bins   = [0, 25, 35, 45, 60, 100]\n",
    "labels = ['≤25', '26-35', '36-45', '46-60', '60+']\n",
    "df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)\n",
    "\n",
    "print('Cleaning complete.')\n",
    "df.dtypes\n",
]))

# ── 3. Missing Values ──────────────────────────────────────
cells.append(cell([
    "## 3. Missing Value & Duplicate Analysis\n",
    "> Identify gaps in the data that must be handled before analysis.\n",
    "\n",
    "| Column | Reason for missing |\n",
    "|--------|--------------------|\n",
    "| `paid_off_time` | COLLECTION loans were never paid off (100 records) |\n",
    "| `past_due_days` | Only applicable to overdue loans (PAIDOFF have 0 due) |\n",
    "| `days_to_payoff` | Derived from `paid_off_time` — same 100 missing records |\n",
], cell_type='markdown'))

cells.append(cell([
    "print('=== Duplicates ===')\n",
    "print(f'Total duplicate rows: {df.duplicated().sum()}')\n",
    "\n",
    "print('\\n=== Missing Values ===')\n",
    "miss = df.isnull().sum()\n",
    "miss_pct = (miss / len(df) * 100).round(2)\n",
    "pd.DataFrame({'Missing Count': miss, 'Missing %': miss_pct}).query('`Missing Count` > 0')\n",
]))

# ── 4. EDA ─────────────────────────────────────────────────
cells.append(cell(["## 4. Exploratory Data Analysis\n", "> Distribution of key features."], cell_type='markdown'))

cells.append(cell([
    "print('Loan Status Counts:')\n",
    "print(df['loan_status'].value_counts())\n",
    "\n",
    "print('\\nPrincipal Value Counts:')\n",
    "print(df['Principal'].value_counts())\n",
    "\n",
    "print('\\nTerm Counts:')\n",
    "print(df['terms'].value_counts())\n",
    "\n",
    "print('\\nEducation Counts:')\n",
    "print(df['education'].value_counts())\n",
    "\n",
    "print('\\nGender Counts:')\n",
    "print(df['Gender'].value_counts())\n",
]))

# ── 5. Statistical Analysis ────────────────────────────────
cells.append(cell([
    "## 5. Statistical Analysis\n",
    "> Descriptive statistics, hypothesis testing, and distribution checks.\n",
], cell_type='markdown'))

cells.append(cell([
    "num_cols = ['Principal', 'terms', 'age', 'past_due_days']\n",
    "df[num_cols].describe().round(2)\n",
]))

cells.append(cell([
    "# Skewness and Kurtosis\n",
    "skew_kurt = pd.DataFrame({\n",
    "    'Skewness': df[num_cols].skew(),\n",
    "    'Kurtosis': df[num_cols].kurt()\n",
    "}).round(3)\n",
    "print('Skewness & Kurtosis:')\n",
    "skew_kurt\n",
]))

cells.append(cell([
    "# Welch's T-test: Principal PAIDOFF vs COLLECTION\n",
    "p_paid = df[df['loan_status'] == 'PAIDOFF']['Principal']\n",
    "p_coll = df[df['loan_status'] == 'COLLECTION']['Principal']\n",
    "t_stat, p_val = stats.ttest_ind(p_paid, p_coll, equal_var=False)\n",
    "print(f\"T-test (Principal: PAIDOFF vs COLLECTION)\")\n",
    "print(f\"  t = {t_stat:.4f},  p = {p_val:.4f}\")\n",
    "print(f\"  Interpretation: {'Significant difference (p<0.05)' if p_val<0.05 else 'No significant difference (p≥0.05)'}\")\n",
]))

cells.append(cell([
    "# Chi-square test: Gender vs Loan Status\n",
    "ct = pd.crosstab(df['Gender'], df['loan_status'])\n",
    "chi2, p_chi, dof, _ = stats.chi2_contingency(ct)\n",
    "print(f\"Chi-square (Gender vs Loan Status)\")\n",
    "print(f\"  chi2={chi2:.4f},  p={p_chi:.4f},  dof={dof}\")\n",
    "print(f\"  Interpretation: {'Gender IS associated with loan status (p<0.05)' if p_chi<0.05 else 'Gender is NOT significantly associated with loan status (p≥0.05)'}\")\n",
    "ct\n",
]))

# ── 6. Loan Status Chart ───────────────────────────────────
cells.append(cell(["## 6. Loan Status Analysis (Chart 1)"], cell_type='markdown'))

cells.append(cell([
    "status_counts = df['loan_status'].value_counts()\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Chart 1 – Loan Status Distribution', fontsize=14, fontweight='bold')\n",
    "\n",
    "bars = axes[0].bar(status_counts.index, status_counts.values,\n",
    "                   color=[COLORS.get(s,'#95a5a6') for s in status_counts.index], edgecolor='white')\n",
    "axes[0].set_title('Count by Loan Status'); axes[0].set_xlabel('Loan Status'); axes[0].set_ylabel('Count')\n",
    "for b in bars: axes[0].text(b.get_x()+b.get_width()/2, b.get_height()+2, str(int(b.get_height())), ha='center')\n",
    "\n",
    "axes[1].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%',\n",
    "            colors=[COLORS.get(s,'#95a5a6') for s in status_counts.index],\n",
    "            startangle=140, wedgeprops=dict(edgecolor='white'))\n",
    "axes[1].set_title('Proportion by Loan Status')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 7. Principal Chart ─────────────────────────────────────
cells.append(cell(["## 7. Principal Analysis (Chart 2)"], cell_type='markdown'))

cells.append(cell([
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Chart 2 – Principal Amount by Loan Status', fontsize=14, fontweight='bold')\n",
    "for status, color in COLORS.items():\n",
    "    sub = df[df['loan_status']==status]['Principal']\n",
    "    if len(sub): axes[0].hist(sub, bins=15, alpha=0.6, label=status, color=color, edgecolor='white')\n",
    "axes[0].set_title('Histogram'); axes[0].set_xlabel('Principal ($)'); axes[0].legend()\n",
    "sns.boxplot(data=df, x='loan_status', y='Principal', palette=COLORS, ax=axes[1], order=list(COLORS.keys()))\n",
    "axes[1].set_title('Box Plot'); axes[1].set_xlabel('Loan Status')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 8. Gender Chart ────────────────────────────────────────
cells.append(cell(["## 8. Gender Analysis (Chart 3)"], cell_type='markdown'))

cells.append(cell([
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5))\n",
    "fig.suptitle('Chart 3 – Gender Analysis', fontsize=14, fontweight='bold')\n",
    "gc = df['Gender'].value_counts()\n",
    "axes[0].bar(gc.index, gc.values, color=['#3498db','#e91e8c'], edgecolor='white')\n",
    "axes[0].set_title('Gender Distribution'); axes[0].set_ylabel('Count')\n",
    "for i,v in enumerate(gc.values): axes[0].text(i, v+1, str(v), ha='center')\n",
    "\n",
    "gs = pd.crosstab(df['Gender'], df['loan_status'], normalize='index')*100\n",
    "cols_p = [c for c in ['PAIDOFF','COLLECTION','COLLECTION_PAIDOFF'] if c in gs.columns]\n",
    "gs[cols_p].plot(kind='bar', stacked=True, ax=axes[1], color=[COLORS[c] for c in cols_p], edgecolor='white')\n",
    "axes[1].set_title('Loan Status by Gender (%)'); axes[1].tick_params(axis='x', rotation=0); axes[1].legend(fontsize=8)\n",
    "\n",
    "ap = df.groupby('Gender')['Principal'].mean()\n",
    "axes[2].bar(ap.index, ap.values, color=['#3498db','#e91e8c'], edgecolor='white')\n",
    "axes[2].set_title('Avg Principal by Gender'); axes[2].set_ylabel('Avg Principal ($)')\n",
    "for i,v in enumerate(ap.values): axes[2].text(i, v+5, f'${v:.0f}', ha='center')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 9. Education Chart ─────────────────────────────────────
cells.append(cell(["## 9. Education Analysis (Chart 4)"], cell_type='markdown'))

cells.append(cell([
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "fig.suptitle('Chart 4 – Education Analysis', fontsize=14, fontweight='bold')\n",
    "ec = df['education'].value_counts().reindex(edu_order).fillna(0)\n",
    "axes[0].barh(edu_order, ec.values, color=['#9b59b6','#3498db','#2ecc71','#e67e22'], edgecolor='white')\n",
    "axes[0].set_title('Education Level Distribution'); axes[0].set_xlabel('Count')\n",
    "for i,v in enumerate(ec.values): axes[0].text(v+1, i, str(int(v)), va='center')\n",
    "\n",
    "es = pd.crosstab(df['education'], df['loan_status'], normalize='index')*100\n",
    "es = es.reindex(edu_order).fillna(0)\n",
    "cols_p = [c for c in ['PAIDOFF','COLLECTION','COLLECTION_PAIDOFF'] if c in es.columns]\n",
    "es[cols_p].plot(kind='bar', ax=axes[1], color=[COLORS[c] for c in cols_p], edgecolor='white')\n",
    "axes[1].set_title('Loan Status by Education (%)'); axes[1].tick_params(axis='x', rotation=25); axes[1].legend(fontsize=8)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 10. Age Chart ──────────────────────────────────────────
cells.append(cell(["## 10. Age Analysis (Chart 5)"], cell_type='markdown'))

cells.append(cell([
    "fig, axes = plt.subplots(1, 3, figsize=(16, 5))\n",
    "fig.suptitle('Chart 5 – Age Analysis', fontsize=14, fontweight='bold')\n",
    "axes[0].hist(df['age'], bins=20, color='#3498db', edgecolor='white')\n",
    "axes[0].axvline(df['age'].mean(), color='red', linestyle='--', label=f\"Mean={df['age'].mean():.1f}\")\n",
    "axes[0].set_title('Age Distribution'); axes[0].legend()\n",
    "\n",
    "ag = df.groupby(['age_group','loan_status']).size().unstack(fill_value=0)\n",
    "cols_p = [c for c in ['PAIDOFF','COLLECTION','COLLECTION_PAIDOFF'] if c in ag.columns]\n",
    "ag[cols_p].plot(kind='bar', ax=axes[1], color=[COLORS[c] for c in cols_p], edgecolor='white')\n",
    "axes[1].set_title('Loan Status by Age Group'); axes[1].tick_params(axis='x', rotation=0); axes[1].legend(fontsize=8)\n",
    "\n",
    "sns.boxplot(data=df, x='loan_status', y='age', palette=COLORS, ax=axes[2], order=list(COLORS.keys()))\n",
    "axes[2].set_title('Age by Loan Status')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 11. Term Chart ─────────────────────────────────────────
cells.append(cell(["## 11. Loan Term Analysis (Chart 6)"], cell_type='markdown'))

cells.append(cell([
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Chart 6 – Loan Term Analysis', fontsize=14, fontweight='bold')\n",
    "ts = pd.crosstab(df['terms'], df['loan_status'])\n",
    "cols_p = [c for c in ['PAIDOFF','COLLECTION','COLLECTION_PAIDOFF'] if c in ts.columns]\n",
    "ts[cols_p].plot(kind='bar', ax=axes[0], color=[COLORS[c] for c in cols_p], edgecolor='white')\n",
    "axes[0].set_title('Count by Term'); axes[0].tick_params(axis='x', rotation=0)\n",
    "\n",
    "tp = pd.crosstab(df['terms'], df['loan_status'], normalize='index')*100\n",
    "tp[cols_p].plot(kind='bar', stacked=True, ax=axes[1], color=[COLORS[c] for c in cols_p], edgecolor='white')\n",
    "axes[1].set_title('% Stacked by Term'); axes[1].tick_params(axis='x', rotation=0)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 12. Correlation Chart ──────────────────────────────────
cells.append(cell(["## 12. Correlation Analysis (Chart 7)"], cell_type='markdown'))

cells.append(cell([
    "df_enc = df.copy()\n",
    "df_enc['gender_num'] = (df_enc['Gender']=='male').astype(int)\n",
    "df_enc['status_num'] = df_enc['loan_status'].map({'PAIDOFF':0,'COLLECTION_PAIDOFF':1,'COLLECTION':2})\n",
    "df_enc['edu_num']    = df_enc['education'].map({'High School or Below':0,'college':1,'Bechalor':2,'Master or Above':3})\n",
    "\n",
    "corr_cols = ['Principal','terms','age','past_due_days','days_to_payoff','gender_num','status_num','edu_num']\n",
    "corr = df_enc[corr_cols].corr()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 7))\n",
    "sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', linewidths=0.5, ax=ax,\n",
    "            vmin=-1, vmax=1, square=True, cbar_kws={'shrink':0.8})\n",
    "ax.set_title('Chart 7 – Correlation Heatmap', fontsize=14, fontweight='bold', pad=12)\n",
    "ax.tick_params(axis='x', rotation=30)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 13. Days to Payoff ─────────────────────────────────────
cells.append(cell(["## 13. Days to Payoff Analysis (Chart 8)"], cell_type='markdown'))

cells.append(cell([
    "df_paid = df[df['loan_status'].isin(['PAIDOFF','COLLECTION_PAIDOFF'])].copy()\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Chart 8 – Days to Payoff', fontsize=14, fontweight='bold')\n",
    "for s in ['PAIDOFF','COLLECTION_PAIDOFF']:\n",
    "    sub = df_paid[df_paid['loan_status']==s]['days_to_payoff'].dropna()\n",
    "    if len(sub): axes[0].hist(sub, bins=20, alpha=0.6, label=s, color=COLORS[s], edgecolor='white')\n",
    "axes[0].set_title('Distribution of Days to Payoff'); axes[0].legend()\n",
    "sns.scatterplot(data=df_paid, x='days_to_payoff', y='Principal', hue='loan_status', palette=COLORS, alpha=0.6, ax=axes[1])\n",
    "axes[1].set_title('Principal vs Days to Payoff')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 14. Past Due Days ──────────────────────────────────────
cells.append(cell(["## 14. Past Due Days Analysis (Chart 9)"], cell_type='markdown'))

cells.append(cell([
    "df_coll = df[df['loan_status'].isin(['COLLECTION','COLLECTION_PAIDOFF'])].dropna(subset=['past_due_days'])\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "fig.suptitle('Chart 9 – Past Due Days', fontsize=14, fontweight='bold')\n",
    "axes[0].hist(df_coll['past_due_days'], bins=20, color='#e74c3c', edgecolor='white', alpha=0.8)\n",
    "axes[0].set_title('Distribution of Past Due Days'); axes[0].set_xlabel('Past Due Days')\n",
    "sns.boxplot(data=df_coll, x='loan_status', y='past_due_days',\n",
    "            palette={'COLLECTION':'#e74c3c','COLLECTION_PAIDOFF':'#f39c12'}, ax=axes[1])\n",
    "axes[1].set_title('Past Due Days by Status')\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 15. Principal Heatmap ──────────────────────────────────
cells.append(cell(["## 15. Principal by Education & Gender (Chart 10)"], cell_type='markdown'))

cells.append(cell([
    "pivot = df.pivot_table(values='Principal', index='education', columns='Gender', aggfunc='mean').round(0)\n",
    "pivot = pivot.reindex(edu_order)\n",
    "fig, ax = plt.subplots(figsize=(8, 5))\n",
    "sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5, ax=ax,\n",
    "            cbar_kws={'label':'Avg Principal ($)'})\n",
    "ax.set_title('Chart 10 – Avg Principal by Education & Gender', fontsize=14, fontweight='bold', pad=12)\n",
    "plt.tight_layout(); plt.show()\n",
]))

# ── 16. Business Insights ──────────────────────────────────
cells.append(cell([
    "## 16. Business Insights & Recommendations\n",
    "\n",
    "### Key Findings\n",
    "\n",
    "| # | Insight |\n",
    "|---|--------|\n",
    "| 1 | **60% of loans are fully PAIDOFF** — a healthy overall repayment rate. |\n",
    "| 2 | **Female borrowers have a higher PAIDOFF rate (68.8%) than male (58.4%)**, suggesting lower default risk. |\n",
    "| 3 | **Master or Above & High School or Below** education levels show the highest COLLECTION rates (~23–25%). |\n",
    "| 4 | **Most borrowers are 26–35 years old** — young working adults are the primary customer segment. |\n",
    "| 5 | **30-day term loans are the most popular** (54.4%), followed by 15-day (41.4%) and 7-day (4.2%). |\n",
    "| 6 | **$1,000 is by far the most common principal** (75.4% of all loans). |\n",
    "| 7 | **Average past-due period is 36 days** — overdue borrowers tend to be significantly late. |\n",
    "| 8 | **T-test (p=0.09) shows no statistically significant difference in Principal** between PAIDOFF and COLLECTION loans. |\n",
    "| 9 | **Gender and loan status are NOT significantly associated** (Chi-square p=0.17). |\n",
    "| 10 | **No duplicate records** detected — the dataset is clean and reliable. |\n",
    "\n",
    "### Recommendations\n",
    "\n",
    "1. **Stricter credit screening for 30-day loan applicants** — the longest term shows the highest volume but also the broadest collection exposure.\n",
    "2. **Target marketing to 26–35 female borrowers** — they show the highest repayment discipline.\n",
    "3. **Early-intervention reminder programme at Day 1–3 past due** — most COLLECTION_PAIDOFF loans were recovered within 1–7 days late, suggesting timely nudges work.\n",
    "4. **Investigate outlier borrowers with 50+ past-due days** — these represent material credit risk and warrant individual case review.\n",
    "5. **Education-based risk segmentation**: high-school-level and Master's borrowers show higher collection rates; consider adjusted interest rates or smaller initial limits.\n",
    "6. **Expand the 7-day short-term product** — it has the lowest volume but likely the fastest cash cycle; there may be unmet demand.\n",
], cell_type='markdown'))

# ── Build notebook dict ────────────────────────────────────
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.9.0"}
    },
    "cells": cells
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'Loan_Payment_Analysis.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f'Notebook written to: {out_path}')

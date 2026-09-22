# Loan Payment Data Analysis

A complete **Data Analytics project** built on the IBM-style Loan Payments dataset (500 records).  
Submitted as a college Data Analytics project.

---

## Project Structure

```
Loan_Payment_Analysis/
├── analysis.py                        # Main Python analytics script
├── create_notebook.py                 # Script to regenerate the .ipynb
├── Loan_Payment_Analysis.ipynb        # Jupyter Notebook (16 sections)
├── Loan_Payment_Analysis_Report.docx  # Professional DOCX report with charts
├── Loan_Payment_Analysis_Slides.pptx  # PowerPoint presentation
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── charts/
    ├── chart1_loan_status_distribution.png
    ├── chart2_principal_by_status.png
    ├── chart3_gender_analysis.png
    ├── chart4_education_analysis.png
    ├── chart5_age_analysis.png
    ├── chart6_term_analysis.png
    ├── chart7_correlation_heatmap.png
    ├── chart8_days_to_payoff.png
    ├── chart9_past_due_days.png
    └── chart10_principal_edu_gender_heatmap.png
```

---

## Dataset

| Property | Value |
|---|---|
| File | `https://www.kaggle.com/datasets/zhijinzhai/loandata` |
| Records | 500 |
| Columns | 11 |
| Loan Statuses | PAIDOFF (300), COLLECTION (100), COLLECTION_PAIDOFF (100) |

**Columns:**  
`Loan_ID`, `loan_status`, `Principal`, `terms`, `effective_date`, `due_date`,  
`paid_off_time`, `past_due_days`, `age`, `education`, `Gender`

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Python Script (generates all charts)

```bash
python analysis.py
```

> **Note:** Place `Loan payments data.csv` one level above `Loan_Payment_Analysis/`
> (i.e., in the parent folder), or adjust `DATA_PATH` in `analysis.py`.

### 3. Open the Jupyter Notebook

```bash
jupyter notebook Loan_Payment_Analysis.ipynb
```

---

## Analysis Performed

1. **Data Loading** — CSV loading, shape inspection, data types
2. **Data Cleaning** — Date parsing, text standardisation, feature engineering (`days_to_payoff`, `age_group`)
3. **Missing Value & Duplicate Analysis** — 100 missing `paid_off_time` (COLLECTION loans), 300 missing `past_due_days` (PAIDOFF have none)
4. **EDA** — Distributions of all key variables
5. **Statistical Analysis** — Descriptive stats, Welch's T-test, Chi-square test
6. **Loan Status Analysis** — 60% PAIDOFF / 20% COLLECTION / 20% COLLECTION_PAIDOFF
7. **Gender Analysis** — Female PAIDOFF rate 68.8% vs Male 58.4%
8. **Education Analysis** — HS/Below and Master or Above show highest collection rates
9. **Age Analysis** — Mean age 31.1 years; 26–35 age group dominates
10. **Loan Term Analysis** — 30-day term most popular (54.4%)
11. **Correlation Analysis** — Heatmap of 8 encoded variables
12. **Days to Payoff** — COLLECTION_PAIDOFF loans take longer (late payers)
13. **Past Due Days** — Mean overdue period 36 days; max 76 days

---

## Charts Generated

| Chart | Description |
|---|---|
| Chart 1 | Loan Status Distribution (Bar + Pie) |
| Chart 2 | Principal Amount by Loan Status (Histogram + Box Plot) |
| Chart 3 | Gender Analysis (Distribution, Loan Status %, Avg Principal) |
| Chart 4 | Education Analysis (Distribution + Loan Status %) |
| Chart 5 | Age Analysis (Histogram, Status by Age Group, Box Plot) |
| Chart 6 | Loan Term Analysis (Count + % Stacked) |
| Chart 7 | Correlation Heatmap (8 variables) |
| Chart 8 | Days to Payoff (Histogram + Scatter) |
| Chart 9 | Past Due Days (Histogram + Box Plot) |
| Chart 10 | Average Principal by Education & Gender (Heatmap) |

---

## Key Business Insights

1. **60% of loans are successfully PAIDOFF** — healthy portfolio
2. **Female borrowers have a 10-point higher repayment rate** than males
3. **26–35 age group** is the largest and most creditworthy segment
4. **$1,000 / 30-day loans** are the dominant product
5. **Average overdue period is 36 days** for delinquent loans
6. **T-test**: No statistically significant difference in principal amount between PAIDOFF and COLLECTION groups
7. **Chi-square**: Gender is not a statistically significant predictor of loan status
8. High-school-level borrowers show a 23.4% collection rate — the second highest

---

## Recommendations

- Implement early-intervention reminders at Day 1–3 past due
- Offer reduced limits to first-time high-school-level borrowers
- Expand 7-day micro-loan product to meet short-term demand
- Target female 26–35 borrowers for premium / repeat loan products

---

## Tools & Libraries

| Library | Purpose |
|---|---|
| pandas | Data loading, cleaning, manipulation |
| numpy | Numerical operations |
| matplotlib | Charting and visualisation |
| seaborn | Statistical visualisation |
| scipy | Hypothesis testing |
| python-docx | DOCX report generation |
| python-pptx | PowerPoint generation |
| jupyter | Interactive notebook |

---

*Prepared for college Data Analytics project and viva.*

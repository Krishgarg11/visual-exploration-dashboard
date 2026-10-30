# Executive Business Report: Café Chain Annual Sales & Operational Performance (FY 2025)

**Prepared for:** Executive Leadership & Regional Outlet Management  
**Reporting Period:** 1 January 2025 – 31 December 2025  
**Scope:** Performance audit across 3 regional outlets (Pune, Jaipur, Kochi) and 3 product categories (Beverages, Bakery, Merchandise)

---

## 1. Executive Summary & Purpose

This report evaluates annual revenue performance, seasonal dynamics, and promotional elasticity across our three café outlets in 2025, providing management with data-driven insights to optimize staffing, inventory allocation, and promotional expenditure for the upcoming fiscal year.

Across 3,282 audited daily sales records, the café network generated **₹920.6 million** in gross revenue, with an average daily sales line yield of **₹281 thousand**.

---

## 2. Key Findings

* **December Winter Peak:** December is our highest revenue month at **₹102.9 million**, delivering a **27.5% uplift over November (₹80.7 million)**, with January also remaining elevated (**₹82.7 million**). Revenue reaches its annual trough in February (**₹64.6 million**) before embarking on steady month-over-month growth.
* **Predictable Weekend Surge:** Weekend sales (Saturday: **₹341.0k**, Sunday: **₹350.8k**) outperform weekday averages (**₹256.6k**) by **34.8% to 35.1%**. This weekend surge is uniform across all menu categories, including Merchandise (**+34.8% lift**), demonstrating that customer footfall, rather than category-specific demand, drives weekend performance.
* **Pune Outperforms Across All Categories:** Pune is our top-performing outlet, generating **₹337.8 million (36.7% network share)**. Pune leads Kochi and Jaipur in every single product category, averaging **₹488k per beverage line** compared to **₹438k in Kochi** and **₹415k in Jaipur**. Beverages represent our core revenue driver network-wide (**₹467.2 million**, 50.8% of total revenue).

---

## 3. Data Quality & Outlier Investigation Note

During initial data auditing, three extreme anomalous records were detected:
1. **Row 300 (2025-02-03, Jaipur, Beverages):** Reported revenue of **₹2,441.6k**
2. **Row 1800 (2025-07-20, Pune, Beverages):** Reported revenue of **₹3,294.2k**
3. **Row 2900 (2025-11-19, Pune, Merchandise):** Reported revenue of **₹1,055.6k**

**Root-Cause Assessment & Decision:**
A single beverage line generating ₹3.3 million on a quiet July weekday is physically implausible given average line volumes of ₹488k. These records exhibited the characteristic signature of 7x data-entry transcription errors. Applying an item-specific threshold rule (`Revenue <= 3 × Item Mean`) isolated and excised **exactly these 3 erroneous rows**, reducing total rows from 3,285 to 3,282.

Crucially, legitimate high-volume transactions—such as winter weekend beverage sales in Pune reaching ₹959.5k on 28 December—were preserved because they align with established seasonal and operational drivers. Testing an outlet-level threshold (`3 × Outlet Mean`) proved overly blunt, erroneously discarding 4 valid peak trading days due to product mix differences.

---

## 4. Actionable Business Recommendations

1. **Mobilize Winter & Weekend Operational Capacity:**  
   * **Action:** Calibrate procurement contracts and barista roster schedules to accommodate the 35% weekend lift year-round, and scale up inventory buffer stocks by 30% beginning the third week of November through mid-January.
   * **Expected Impact:** Minimizes stock-outs during peak December margin windows and eliminates service bottlenecks.

2. **Replicate Pune's Beverage Execution Playbook in Kochi and Jaipur:**  
   * **Action:** Conduct an operational audit of Pune’s barista workflows, speed-of-service protocols, and upselling scripts, followed by a 30-day pilot implementation in Kochi and Jaipur starting next month.
   * **Expected Impact:** Closing even half of the ₹50k–₹73k per-line gap between Pune and peer outlets on beverages would yield an estimated **₹25–35 million** in incremental annual revenue.

3. **Restructure Promotional Discount Tiers Beyond 20%:**  
   * **Action:** Eliminate the 25% discount tier or replace it with targeted bundling, as average revenue plateaus between 20% (₹305.7k) and 25% (₹304.7k), yielding a negative marginal revenue return (-₹1.1k) while unnecessarily diluting product margins.

---

## 5. Analytical Reference Tables

### Table 1: Annual Revenue Summary by Outlet & Category (₹ Millions)
| Outlet | Beverages | Bakery | Merchandise | Total Revenue | Network Share (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pune** | ₹178.2 M | ₹105.1 M | ₹53.3 M | **₹336.5 M** | **36.6%** |
| **Kochi** | ₹159.8 M | ₹95.6 M | ₹48.0 M | **₹303.3 M** | **32.9%** |
| **Jaipur** | ₹151.4 M | ₹90.7 M | ₹45.4 M | **₹287.5 M** | **31.2%** |
| **Total** | **₹489.3 M** | **₹291.4 M** | **₹146.7 M** | **₹927.4 M** | **100.0%** |
*(Note: Pre-cleaning raw network total ₹927.4M; cleaned audited total ₹920.6M after removing ₹6.8M in clerical errors).*

### Table 2: Promotional Offer Tier Sensitivity
| Offer Tier (%) | Avg Revenue (₹ k) | Step Change (₹ k) | Marginal Return Observation |
| :---: | :---: | :---: | :--- |
| **0%** | ₹253.2 k | Baseline | Standard baseline transactions |
| **5%** | ₹260.7 k | +₹7.5 k | Modest initial lift (+3.0%) |
| **10%** | ₹284.0 k | +₹23.3 k | Significant acceleration (+8.9%) |
| **15%** | ₹285.6 k | +₹1.6 k | Flattening curve (+0.6%) |
| **20%** | ₹305.7 k | +₹20.2 k | Secondary surge (+7.0%) |
| **25%** | ₹304.7 k | -₹1.1 k | Negative marginal lift; margin degradation |

---
*Report certified by Senior Data Analyst & Visualization Team.*

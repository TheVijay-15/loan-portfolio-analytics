import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

conn = sqlite3.connect('loan_analysis.db')

print("📊 Creating Visualizations...")

# 1. RISK VS REWARD BY GRADE
plt.figure(figsize=(12, 6))

# Calculate metrics by grade
risk_data = pd.read_sql("""
    SELECT 
        grade,
        AVG(int_rate) as avg_interest_rate,
        (SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as default_rate_percent
    FROM lending_club_loans 
    GROUP BY grade
    ORDER BY grade
""", conn)

# Create the plot
plt.subplot(1, 2, 1)
bars = plt.bar(risk_data['grade'], risk_data['avg_interest_rate'], alpha=0.7, color='skyblue')
plt.plot(risk_data['grade'], risk_data['default_rate_percent'], color='red', marker='o', linewidth=3, markersize=8, label='Default Rate %')
plt.title('Risk vs Reward by Credit Grade')
plt.xlabel('Credit Grade')
plt.ylabel('Percentage')
plt.legend()
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, risk_data['avg_interest_rate']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{value:.1f}%', 
             ha='center', va='bottom', fontsize=9)

# 2. DEFAULT RATE BY EMPLOYMENT LENGTH (FIXED)
plt.subplot(1, 2, 2)
emp_data = pd.read_sql("""
    SELECT 
        CASE 
            WHEN emp_length IS NULL THEN 'Not Provided'
            ELSE emp_length 
        END as emp_length,
        (SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as default_rate_percent
    FROM lending_club_loans 
    GROUP BY emp_length
    ORDER BY default_rate_percent DESC
""", conn)

# Convert to list to handle None values
emp_lengths = list(emp_data['emp_length'])
default_rates = list(emp_data['default_rate_percent'])

bars = plt.bar(range(len(emp_lengths)), default_rates, color='lightcoral')
plt.title('Default Rate by Employment Length')
plt.xlabel('Employment Length')
plt.ylabel('Default Rate %')
plt.xticks(range(len(emp_lengths)), emp_lengths, rotation=45, ha='right')
plt.grid(True, alpha=0.3)

# Add value labels
for i, value in enumerate(default_rates):
    plt.text(i, value + 1, f'{value:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# 3. LOAN PURPOSE PROFITABILITY
plt.figure(figsize=(12, 6))
purpose_data = pd.read_sql("""
    SELECT 
        purpose,
        SUM(total_pymnt - loan_amnt) as net_profit
    FROM lending_club_loans 
    GROUP BY purpose
    ORDER BY net_profit DESC
""", conn)

# Convert to lists to handle any data issues
purposes = list(purpose_data['purpose'])
profits = list(purpose_data['net_profit'])

colors = ['green' if x > 0 else 'red' for x in profits]
bars = plt.bar(range(len(purposes)), profits, color=colors, alpha=0.7)
plt.title('Profitability by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Net Profit ($)')
plt.xticks(range(len(purposes)), purposes, rotation=45, ha='right')
plt.grid(True, alpha=0.3)

# Add value labels
for i, value in enumerate(profits):
    plt.text(i, value + 500, f'${value:,.0f}', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()

conn.close()
print("✅ Visualizations created successfully!")
import pandas as pd
import sqlite3

def get_portfolio_summary():
    conn = sqlite3.connect('loan_analysis.db')
    
    summary = pd.read_sql("""
        SELECT 
            COUNT(*) as total_loans,
            SUM(loan_amnt) as total_portfolio_value,
            AVG(loan_amnt) as avg_loan_size,
            AVG(int_rate) as avg_interest_rate,
            SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) as total_defaults,
            (SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as default_rate_percent,
            SUM(total_pymnt) as total_collections,
            (SUM(total_pymnt) - SUM(loan_amnt)) as net_profit
        FROM lending_club_loans
    """, conn)
    
    conn.close()
    return summary

def get_risk_by_grade():
    conn = sqlite3.connect('loan_analysis.db')
    
    risk_data = pd.read_sql("""
        SELECT 
            grade,
            COUNT(*) as total_loans,
            AVG(loan_amnt) as avg_loan_amount,
            AVG(int_rate) as avg_interest_rate,
            SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) as defaults,
            (SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as default_rate_percent,
            SUM(total_pymnt - loan_amnt) as net_profit
        FROM lending_club_loans 
        GROUP BY grade
        ORDER BY grade
    """, conn)
    
    conn.close()
    return risk_data

def get_profitability_by_purpose():
    conn = sqlite3.connect('loan_analysis.db')
    
    profit_data = pd.read_sql("""
        SELECT 
            purpose,
            COUNT(*) as total_loans,
            AVG(loan_amnt) as avg_loan_size,
            AVG(int_rate) as avg_interest_rate,
            SUM(total_pymnt) as total_collections,
            SUM(total_pymnt - loan_amnt) as net_profit,
            (SUM(total_pymnt - loan_amnt) * 100.0 / SUM(loan_amnt)) as roi_percent
        FROM lending_club_loans 
        GROUP BY purpose
        ORDER BY net_profit DESC
    """, conn)
    
    conn.close()
    return profit_data

if __name__ == "__main__":
    print("📊 Running Analysis...")
    print(get_portfolio_summary())
    print(get_risk_by_grade())
    print(get_profitability_by_purpose())
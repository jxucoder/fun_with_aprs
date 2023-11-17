import streamlit as st
import numpy_financial as npf
import numpy as np
import pandas as pd
import altair as alt


def calculate_compound_interest_payments(loan_amount, apr, monthly_payment):
    # Convert APR to monthly interest rate
    monthly_interest_rate = apr / 12

    # Calculate the number of periods using numpy's financial functions
    num_periods = npf.nper(monthly_interest_rate, -monthly_payment, loan_amount)

    # Lists to store monthly principal and interest payments
    principal_payments = []
    interest_payments = []

    # Initialize the current balance to the loan amount
    current_balance = loan_amount

    for _ in range(int(num_periods)):
        # Calculate interest for the current month
        monthly_interest = current_balance * monthly_interest_rate

        # Calculate principal for the current month
        monthly_principal = monthly_payment - monthly_interest

        # Update the current balance
        current_balance -= monthly_principal

        # Append principal and interest payments to their respective lists
        principal_payments.append(round(monthly_principal, 2))
        interest_payments.append(round(monthly_interest, 2))

    return principal_payments, interest_payments


def calculate_simple_interest_payments(loan_amount, apr, num_periods):
    """
    Calculate principal and interest payments for a loan.

    Parameters:
        loan_amount (float): The total loan amount.
        apr (float): The annual percentage rate (APR) as a decimal.
        num_periods (int): The number of payment periods.

    Returns:
        principal_payments (list): List of principal payments per period.
        interest_payments (list): List of interest payments per period.
    """
    monthly_rate = apr / 12  # Convert APR to monthly rate
    monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -num_periods)

    principal_remaining = loan_amount
    principal_payments = []
    interest_payments = []

    for _ in range(num_periods):
        interest_payment = principal_remaining * monthly_rate
        principal_payment = monthly_payment - interest_payment

        principal_remaining -= principal_payment
        principal_payments.append(principal_payment)
        interest_payments.append(interest_payment)

    return principal_payments, interest_payments


if __name__ == "__main__":
    st.set_page_config(layout='wide')

    with st.sidebar:
        st.title("Simpler is Better")
        loan_amount = st.slider('Loan Amount', min_value=500, max_value=2000, step=100, value=1000)
        apr = st.select_slider('APR', options=['0%', '10%', '20%', '30%', '36%'], value='20%')
        apr_num = int(apr[:-1])/100
        with st.expander("Option 1: Simple Interests", expanded=True):
            installment_num = st.slider('Number of Installments', min_value=3, max_value=18, step=3, value=12)

        with st.expander("Option 2: Compound Interests", expanded=True):
            # period_num = st.slider('Number of Months', min_value=3, max_value=18, step=3, value=12)
            monthly_payment_num = st.slider('Loan Amount', min_value=25, max_value=round(loan_amount / 3 / 50) * 50, step=50)

    simple_principal_payments, simple_interest_payments = \
        calculate_simple_interest_payments(loan_amount, apr_num, installment_num)

    compound_principal_payments, compound_interest_payments = \
        calculate_compound_interest_payments(loan_amount, apr_num, monthly_payment_num)

    col_simple, col_compound = st.columns(2)

    with col_simple:
        st.subheader("Installment Credit")
        st.write(f"total interests {sum(simple_interest_payments)}")
        months = [i for i in range(1, len(simple_principal_payments)+1)]
        df_simple = pd.DataFrame({
            'Month': months,
            'Principal Payments': simple_principal_payments,
            'Interest Payments': simple_interest_payments,
        })
        df_simple = df_simple.melt(id_vars="Month", var_name="Type", value_name="Payment")  # reshape for Altair chart

        st.altair_chart(alt.Chart(df_simple)
            .mark_bar()
            .encode(
                x='Payment',
                y='Month:O',  # 'O' indicates ordinal data
                color='Type',
                order=alt.Order(
                    'Type',
                    sort='ascending'
                )
            )
        )

    with col_compound:
        st.subheader("Revolving Credit")
        st.write(f"total interests {sum(compound_interest_payments)}")

        months = [i for i in range(1, len(compound_interest_payments) + 1)]
        df_simple = pd.DataFrame({
            'Month': months,
            'Interest Payments': compound_interest_payments,
            'Principal Payments': compound_principal_payments,
        })
        df_simple = df_simple.melt(id_vars="Month", var_name="Type", value_name="Payment")  # reshape for Altair chart

        st.altair_chart(alt.Chart(df_simple)
            .mark_bar()
            .encode(
            x='Payment',
            y='Month:O',  # 'O' indicates ordinal data
            color='Type',
            order=alt.Order(
                'Type',
                sort='ascending'
            )
        )
        )
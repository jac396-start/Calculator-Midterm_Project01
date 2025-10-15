import pandas as pd
import os

HISTORY_FILE = 'calculation_history.csv'

def save_history(history_df):
    """Saves the calculation history DataFrame to a CSV file."""
    try:
        history_df.to_csv(HISTORY_FILE, index=False)
        print(f"\nCalculation history saved to {HISTORY_FILE}")
    except Exception as e:
        print(f"\nError saving history: {e}")

def load_history():
    """Loads calculation history from a CSV file."""
    if os.path.exists(HISTORY_FILE):
        try:
            history_df = pd.read_csv(HISTORY_FILE)
            print(f"\nCalculation history loaded from {HISTORY_FILE}")
            return history_df
        except Exception as e:
            print(f"\nError loading history: {e}")
            return pd.DataFrame(columns=['operation', 'operands', 'result']) # Return empty DataFrame on error
    else:
        print("\nNo existing calculation history found.")
        return pd.DataFrame(columns=['operation', 'operands', 'result']) # Return empty DataFrame if file doesn't exist

if __name__ == "__main__":
    # Ensure installation check runs first (already in the file)
    # install_pandas_if_not_installed()

    # Load existing history or create a new one
    calculation_history_df = load_history()
    print("\nCurrent Calculation History:")
    print(calculation_history_df)

    # --- Example of adding a calculation to history ---
    new_calculation = {'operation': 'add', 'operands': '1, 2', 'result': '3'}
    calculation_history_df = pd.concat([calculation_history_df, pd.DataFrame([new_calculation])], ignore_index=True)

    new_calculation = {'operation': 'subtract', 'operands': '5, 3', 'result': '2'}
    calculation_history_df = pd.concat([calculation_history_df, pd.DataFrame([new_calculation])], ignore_index=True)

    print("\nHistory after adding new calculations:")
    print(calculation_history_df)

    # --- Example of auto-saving history ---
    save_history(calculation_history_df)

    # Add example pandas code here (already in the file)
    # print("\nDemonstrating pandas usage:")
    # data = {'col1': [1, 2, 3, 4], 'col2': ['A', 'B', 'C', 'D']}
    # df = pd.DataFrame(data)
    # print("\nOriginal DataFrame:")
    # print(df)
    # print("\nSelecting 'col1':")
    # print(df['col1'])
    # print("\nFiltering rows where 'col1' > 2:")
    # print(df[df['col1'] > 2]


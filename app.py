from datetime import datetime

import pandas as pd
import streamlit as st


def prepare_df_to_display(
    csv_path: str,
    cols_to_keep_and_rename: dict[str, str],
    rfm_score_threshold: int = 15,
    rfm_score_col: str = "RFM_score",
    valuable_customer_col: str = "Valuable customer",
    user_cols: tuple[str] = ("opinion",),
) -> pd.DataFrame:
    """
    Prepares a DataFrame for display by keeping specified columns, renaming them,
    and adding a valuable customer column based on an RFM score threshold.

    Args:
        csv_path (str): Path to the CSV file containing the RFM data.
        cols_to_keep_and_rename (dict[str, str]): Dictionary mapping the original column names (keys)
            to the desired new names (values).
        rfm_score_threshold (int, default 15): The minimum RFM score required to mark a client as valuable.
        rfm_score_col (str, default "RFM_score"): Name of the column containing RFM scores.
        valuable_customer_col (str, default "Valuable customer"): Name of the column displaying if customer is valuable.
        user_cols (tuple[str], default ["opinion"]): Columns for the user to fill.
    Returns:
        pd.DataFrame: DataFrame to be displayed, with assessment if customer is valuable based on given threshold.
    """

    rfm_table: pd.DataFrame = pd.read_csv(csv_path)

    rfm_table[valuable_customer_col] = (rfm_table[rfm_score_col] >= rfm_score_threshold).replace(
        {True: "Yes", False: "No"}
    )

    cols_to_display: list[str] = list(cols_to_keep_and_rename.keys()) + [valuable_customer_col]
    rmf_table_to_display: pd.DataFrame = rfm_table[cols_to_display].rename(columns=cols_to_keep_and_rename)

    for col in user_cols:
        rmf_table_to_display[col] = ""

    return rmf_table_to_display


def create_st_editor(table_to_display: pd.DataFrame) -> st.data_editor:
    """Creates table to be displayed as streamlit element."""
    return st.data_editor(
        table_to_display,
        column_config={
            "opinion": st.column_config.SelectboxColumn(
                "Your Opinion",
                help="Do you agree or disagree with the RFM analysis for this customer?",
                width="medium",
                options=[
                    "👍 Agree",
                    "👎 Disagree",
                    "🤷 Not sure",
                ],
            )
        },
        hide_index=True,
        use_container_width=True,
        height=600,
    )


def main():
    table_to_display: pd.DataFrame = prepare_df_to_display(
        csv_path="data/processed/01.0-frosa-customer-transactions-data-bank-rfm-analysis.csv",
        cols_to_keep_and_rename={"customer_id": "Customer ID"},
    )

    st.title("Valuable clients - RFM Analysis")

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    user = st.text_input(
        "Enter your name 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

    table_result: st.data_editor = create_st_editor(table_to_display=table_to_display)

    if st.button("Submit"):
        if not user:
            st.write(":red[Please enter your name before submitting.]")
        else:
            file_name: str = f"{user}_{datetime.now()}.csv"
            table_result.to_csv(f"data/user_output/{file_name}")
            st.write("Submission successful.")


if __name__ == "__main__":
    main()

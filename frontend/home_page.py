import streamlit as st
from pandas import DataFrame, to_datetime
from src.library.overview_helper.overview_functions import check_connection, get_wallet_balances, get_logo_header
from library.ui_elements import fix_padding_top_and_footer


st.set_page_config(layout="wide")
fix_padding_top_and_footer()

check_connection()

get_logo_header()
st.write('Overview of Account and Wallet Balance')


get_wallet_balances()

wo_tab, tab2 = st.tabs(['Wallet Overview', 'Tab 2'])


with wo_tab:
    st.info('💡 The locked assets in Binance are not yet available to show.')
    st.selectbox('Choose Exchange Account', options=['Binance', 'Coinbase', 'Crypto.com', 'Gemini','Kraken',  'KuCoin'], disabled=True, help="Support for Coinbase, Crypto.com, Gemini, Kraken, KuCoin TBA")

with tab2:
    st.write('Tab 2')

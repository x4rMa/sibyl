import streamlit as st
from frontend.src.library.ui_elements import fix_page_layout
from frontend.src.library.settings_helper.funcs import update_api_credentials
from frontend.src.library.client import check_exchange_api_connection, check_backend_connection
from frontend.db.db_connector import update_fields, fetch_fields
from pandas import DataFrame
from settings.settings import UI_VERSION
fix_page_layout('Settings')

st.markdown("""<h2 style='text-align: center;margin-top:0; padding-top:0;'>Settings</h2>""", unsafe_allow_html=True)
st.write('In the Settings Tab ⚙️ you can define the credentials of your Crypto Exchange Account & your personal API keys in order for the Dashboard to operate')
st.sidebar.info(f'⚙️Sibyl Version **{UI_VERSION}**')
st.write('Current User Configurations')

db_fields = fetch_fields()[0]  # frontend DB settings
# print DB settings
df_settings = DataFrame()
df_settings['Configuration'] = ['Exchange', 'Backend Server IP', 'Backend Server Port']
df_settings['Current Parameter'] = [db_fields[1], db_fields[3], db_fields[4]]
st.dataframe(df_settings, hide_index=True)


st.sidebar.button('Reset All Data', type='primary')
# st.write('Current Status')
with st.spinner('Checking Backend Server connection'):
    server_conn = check_backend_connection()

with st.spinner('Checking Crypto Exchange API connection'):
    api_conn = check_exchange_api_connection()

trd_tab, back_tab, api_tab, nlp_tab = st.tabs(['Trading Settings', 'Backend Server Settings', 'Crypto Exchange API Settings', 'NLP Model API Settings'])


with trd_tab:
    with st.form('Trading Parameters'):
        exchange = st.selectbox('Choose Crypto Exchange', options= ['Binance', 'Coinbase', 'Crypto.com', 'Gemini','Kraken',  'KuCoin'], disabled=True, help="Support for Coinbase, Crypto.com, Gemini, Kraken, KuCoin TBA")
        st.info("💡 Currently only Binance is supported, the following will be added: Coinbase, Crypto.com, Gemini, Kraken, KuCoin")
        with st.expander('Betting Options', expanded=True):
            betting_coin = st.selectbox("Choose Betting Coin [recommended: USDT]", ['USDT', 'BNB', 'BTC'], disabled=True)
        trd_submit = st.form_submit_button('Update Trading Parameters')
        if trd_submit:
            # update_betting_options(exchange)
            st.write("ok")
with back_tab:
    with st.form('Backend Server Settings'):
        bcols = st.columns([2, 1])

        serv_ip = st.text_input('Server IP', value=db_fields[3], placeholder="Default: http://127.0.0.1")
        serv_port = st.text_input('Server Port', value=db_fields[4], placeholder="Default: 8000")

        back_submit = st.form_submit_button('Update Server Settings')
        old_serv_adr = db_fields[5]
        if back_submit:
            serv_adr = serv_ip+':'+serv_port
            update_fields(backend_server_ip=serv_ip, backend_server_port=serv_port,backend_server_socket_address=serv_adr)  # Update NLP Model Choice in frontend SQlite3 DB
            st.success(f'Server Parameters Update Successfuly, New Configurations: [{old_serv_adr}] -> [{serv_adr}]')

with api_tab:
    with st.form('Exchange API Credentials'):
        # switch with global
        exchange = st.selectbox('Choose Crypto Exchange', options=['Binance', 'Coinbase'], disabled=True)
        if api_conn:
            st.success('✅ A valid API key is already active.')
        else:
            st.warning('⚠️ No active API Key found on the Server, please initialize.')

        st.caption('In case you have a Binance Account and have not activated the API yet, see instructions below:')
        st.page_link("https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072", label="Binance FAQ", icon="🌐")

        with st.expander('API Credentials', expanded=True):
            st.text_input('API Key', placeholder='Type or Copy/Paste API Key here...', type="password")
            st.text_input('Secret Key', placeholder='Type or Copy/Paste Secret Key here...', type="password")
            st.radio(label="Account Type", options=['Personal', 'Testnet'], horizontal=True)
        api_submit = st.form_submit_button('Update Credentials')
        if api_submit:
            update_api_credentials(exchange)
with nlp_tab:
    with st.form('API Credentials'):
        nlp_model = st.selectbox('Choose NLP LLM Model API', options=['Hugging Face Falcon', 'OpenAI API', 'Google Gemini API'], help="Update NLP Model Choice in frontend SQlite3 DB")
        with st.expander('API Credentials', expanded=True):
            st.text_input('Secret Key', placeholder="Secret Key Input", type="password")
        nlp_submit = st.form_submit_button('Update Credentials')
        if nlp_submit:
            update_fields(nlp_model_choice=nlp_model)  # Update NLP Model Choice in frontend SQlite3 DB
            st.write("ok")

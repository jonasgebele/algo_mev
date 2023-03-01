import streamlit as st
import requests

st.set_page_config(page_title='Algorand Analytics', layout = 'wide', page_icon = './images/logo.jpg')
st.title("Algorand Analytics")

def block_summary(round):
    pass
    #image1 = Image.open("images/algo.png")
    #image2 = Image.open("images/usdt.png")
    #col0, col1, col2, col3, col4, col5 = st.columns([20, 1, 1, 1, 30, 10])
    #col0.write("TxID [2LOER3TT4FUJM6FHQZPME6OX56ZMFP2CTGB3RK5HOX44T7PPHGIA]")
    #col1.image(image1, width=25, use_column_width=False)
    #col2.write("→")
    #col3.image(image2, width=25, use_column_width=False)
    #col4.write("sender: NNEJ6IOFB2D7EUA2VHTFVAUNLY2XZGBMXG5WUW2XJ3IBAJPUW4PNTZ7KIA")
    #col4.write("receiver: SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34")
    #col5.empty()

    if round:
        response = requests.get(f"https://algoindexer.algoexplorerapi.io/v2/blocks/{round}").json()
        if "message" in response and response["message"].startswith("error"):
            st.warning(f"{round} not a valid block-number (round).")
        else:
            st.json(response["transactions"], expanded=False)

def main():
    st.set_page_config(page_title='Algorand Analytics', layout = 'wide', page_icon = './images/logo.jpg')
    st.title("Algorand Analytics")

    round = st.text_input('Block Height (round)', '')
    block_summary(round)

if __name__ == "__main__":
    main()
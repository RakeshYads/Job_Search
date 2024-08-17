import streamlit as st
import requests
import pandas as pd
import json
from app_job_scraping.streamlit_app.preprocessing import naukri
def get_bot_response(user_input):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": user_input}
    response = requests.post(url, json=payload)
    response = json.dumps(response.json())
    response = json.loads(response)
    return response

def load_job_content(jobtitle = None, location = None) -> pd.DataFrame:
    if jobtitle == None and location == None:
        print("Required informatiom are not provided")
    else:
       print("Required details were provided")
       df = naukri.scrape_naukri_func(jobtitle)

    return df

def write_chat_content():
    with st.sidebar:

        message = st.container(height=420)
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "AI", "message": "How can I help you?"}]


        for msg in st.session_state.messages:
            #print(msg)
            #st.chat_message(msg["role"]).write(msg["message"])
            #Source - https://discuss.streamlit.io/t/chatbot-app-with-images-in-chat/61162
            
            for key, value in msg.items():
                if key == 'role':
                    pass
                if key == 'image':
                    with message.chat_message(msg["role"]):
                        st.image(value)
                if key == 'video':
                    with message.chat_message(msg["role"]):
                        st.video(value)
                if key == 'message':
                    with message.chat_message(msg["role"]):
                        st.write(value)

        user_input = st.chat_input()

        if user_input:
            message.chat_message("User").write(user_input)
            st.session_state.messages.append({"role": "User", "message": user_input})
            response = get_bot_response(user_input)
            #response = get_bot_response(user_input)
            # st.chat_message("AI").write(response)
            #st.text_area("Bot Response", value=response, height=200, max_chars=None, key=None)
            #st.session_state.messages.append({"role": "AI", "message": response})
            for res in response:
                #print(res)
                for key, value in res.items():
                    if key == 'recipient_id':
                        pass
                    if key == 'image':
                        # bot_response = bot_response + "https://i.imgur.com/0jD8Y7H.png" + "  \n"
                        # st.chat_message("AI").write(st.image("https://i.imgur.com/0jD8Y7H.png"))
                        message.chat_message("AI").image(value)
                        st.session_state.messages.append({"role": "AI", "image": value})
                    if key == 'text':
                        # bot_response = bot_response + value + "  \n"
                        message.chat_message("AI").write(value)
                        st.session_state.messages.append({"role": "AI", "message": value})
                    if key == 'attachment':
                        # bot_response = bot_response + value + "  \n"
                        values = value['payload']['src']
                        message.chat_message("AI").video(values)
                        st.session_state.messages.append({"role": "AI", "video": values})
                    if key == 'custom':
                        # bot_response = bot_response + value + "  \n"
                        values = value['text']
                        jobtitle = value['jobtitle']
                        location = value['location']
                        df = load_job_content(jobtitle, location)
                        message.chat_message("AI").write(values)
                        message.dataframe(df)
                        st.session_state.messages.append({"role": "AI", "message": values})

def CreateApp():

    st.title("Job Duniya")
    st.subheader("One Stop point to get all the job openings of your desire. Let's search today.")

    write_chat_content()
    st.markdown(
        f'''
            <style>

                section[data-testid="stSidebar"] {{
                    width: 500px !important; # Set the width to your desired value
                }}
                
            </style>
                    ''',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    CreateApp()



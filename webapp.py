import streamlit as st
import requests
import json


def main():
    st.title("Train Your UGAI")

    conversation_id = st.text_input("Either - Enter conversation ID (optional)")

    uploaded_file = st.file_uploader("OR -  Upload a JSON file containing conversation state (optional)", type="json")

    email_recipients = st.text_input("Enter email recipients (comma-separated)")

    if st.button("Train"):
        if conversation_id:
            data_to_send = conversation_id
        elif uploaded_file is not None:
            data_to_send = json.load(uploaded_file)
        else:
            st.warning("Please enter a conversation ID or upload a JSON file.")
            return

        emails_list = [email.strip() for email in email_recipients.split(",")] if email_recipients else []

        payload = {
            "data": data_to_send,
            "email_recipients": emails_list
        }

        url = "https://7c1b-82-163-196-154.ngrok-free.app/train"

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.write("Response from server:")
                st.json(response.json())
            else:
                st.error(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")

    CODE = """
import requests
import json

url = "https://7c1b-82-163-196-154.ngrok-free.app/train"

with open("my_conversation.json", "r") as f:
    conversation_json = json.load(f)

payload_with_json = {
    "data": conversation_json,
    "email_recipients": ["someone@example.com"]
}
resp_json = requests.post(url, json=payload_with_json)
print(resp_json.json())
"""
    st.markdown("## Try it with code")
    st.code(CODE, language="python")


if __name__ == "__main__":
    main()

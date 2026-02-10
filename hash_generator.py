import streamlit_authenticator as stauth

passwords = ["admin123"]  # change if you want a different password
hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords[0])

from app.integration.gmail.auth import get_gmail_credentials

if __name__ == "__main__":
    get_gmail_credentials()
    print("Gmail authentication successful. token.json created.")

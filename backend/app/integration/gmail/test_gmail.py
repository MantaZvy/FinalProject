from app.integration.gmail.service import fetch_application_emails

if __name__ == "__main__":
    emails = fetch_application_emails(5)

    for e in emails:
        print("\n---")
        print("From:", e["from"])
        print("Subject:", e["subject"])
        print("Snippet:", e["snippet"])
from app.integration.gmail.service import fetch_application_emails

if __name__ == "__main__":
    emails = fetch_application_emails(5)
    print("\n Appplication emails found:\n")
    if not emails:
        print("No application emails found.")
    else:
        for e in emails:
            print("\n---")
            print("From:", e["from"])
            print("Subject:", e["subject"])
            print("Snippet:", e["snippet"])
            print("Body:", e["body"][:200])
            print("Status:", e["status"])
            print("-" * 40)
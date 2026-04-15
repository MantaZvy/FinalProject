"""
Evaluation 1: Email Classification Accuracy, tests detect_application_status() function against a synthetic labelled dataset of 30 emails.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#import classifier to test real implementation (detect_application_status function)
from app.integration.gmail.parser import detect_application_status

#30 labelled test emails
TEST_EMAILS = [
    # INTERVIEW (10)
    {"subject": "Interview Invitation – Backend Engineer",
     "body": "We would like to invite you to interview for the Backend Engineer position.", "label": "interview"},
    {"subject": "Next Steps – Software Developer Role",
     "body": "We'd like to invite you to schedule a call to discuss the next stage.", "label": "interview"},
    {"subject": "Exciting Opportunity – Interview Request",
     "body": "We are pleased to invite you for an interview. Please confirm your availability.", "label": "interview"},
    {"subject": "Interview Scheduled – Data Analyst",
     "body": "Further discussion regarding your application. Please confirm availability for an interview.", "label": "interview"},
    {"subject": "We'd love to chat!",
     "body": "We'd like to invite you for a technical interview next week. Please let us know your availability.", "label": "interview"},
    {"subject": "Application Update – Interview Stage",
     "body": "Congratulations on progressing to the next stage. We'd like to schedule an interview.", "label": "interview"},
    {"subject": "Follow up on your application",
     "body": "We were impressed and would like to schedule a call for further discussion.", "label": "interview"},
    {"subject": "Python Developer – Interview Invite",
     "body": "Please confirm your availability for an interview at our offices.", "label": "interview"},
    {"subject": "Talent Acquisition – Next Steps",
     "body": "We are pleased to invite you to the next stage of our hiring process.", "label": "interview"},
    {"subject": "Interview Request – React Developer",
     "body": "We would like to discuss your application further. Are you available for a call?", "label": "interview"},

    # REJECTED (8)
    {"subject": "Your Application – Software Engineer",
     "body": "Unfortunately, we will not be moving forward with your application at this time.", "label": "rejected"},
    {"subject": "Application Decision",
     "body": "We regret to inform you that you have not been selected for this position.", "label": "rejected"},
    {"subject": "Update on Your Application",
     "body": "After careful consideration, we won't be progressing with your candidacy.", "label": "rejected"},
    {"subject": "Re: Application – Data Engineer",
     "body": "We are sorry to inform you that you were unsuccessful in your application.", "label": "rejected"},
    {"subject": "Application Outcome",
     "body": "We have decided not to move forward with your application. We wish you the best.", "label": "rejected"},
    {"subject": "Developer Role – Decision",
     "body": "We regret to inform you that we will not be proceeding with your application.", "label": "rejected"},
    {"subject": "Application Status Update",
     "body": "Unfortunately, you have not been selected to progress to the next stage.", "label": "rejected"},
    {"subject": "Thank you for your interest",
     "body": "We are not moving forward with your application at this time.", "label": "rejected"},

    # APPLIED (7)
    {"subject": "Application Received – Software Engineer",
     "body": "Thank you for applying to the Software Engineer position. We will review your application.", "label": "applied"},
    {"subject": "Thank you for applying to DEVLIFE",
     "body": "Thank you for applying to the Software Engineer Internship. This is an acknowledgement.", "label": "applied"},
    {"subject": "Application Submitted – Google",
     "body": "Your application has been submitted successfully. Thank you for applying.", "label": "applied"},
    {"subject": "We received your application",
     "body": "Thank you for applying. We will be in touch once we have reviewed your application.", "label": "applied"},
    {"subject": "Application Confirmation",
     "body": "Application received. Thank you for submitting your application for the role.", "label": "applied"},
    {"subject": "Thanks for your application",
     "body": "Application submitted. We will review and contact you shortly.", "label": "applied"},
    {"subject": "Application Acknowledgement",
     "body": "Thank you for applying. Your application has been received and is under review.", "label": "applied"},

    # OFFER (5)
    {"subject": "Job Offer – Backend Engineer",
     "body": "We are pleased to offer you the position of Backend Engineer at our company.", "label": "offer"},
    {"subject": "Congratulations! Employment Offer",
     "body": "Congratulations! We would like to extend an offer of employment to you.", "label": "offer"},
    {"subject": "Offer Letter – Software Developer",
     "body": "We are delighted to offer you the role of Software Developer.", "label": "offer"},
    {"subject": "Your Job Offer",
     "body": "Following your interviews, we are pleased to make you a formal job offer.", "label": "offer"},
    {"subject": "Employment Offer – Data Analyst",
     "body": "We are pleased to offer you employment as a Data Analyst starting next month.", "label": "offer"},
]

#METRICS: Accuracy, Precision, Recall, F1 Score
def run():
    y_true, y_pred, results = [], [], []

    for email in TEST_EMAILS:
        predicted = detect_application_status(email["subject"], email["body"])
        y_true.append(email["label"])
        y_pred.append(predicted)

        results.append({
            "subject": email["subject"][:55],
            "expected": email["label"],
            "predicted": predicted,
            "correct": predicted == email["label"]
        })

    correct = sum(r["correct"] for r in results)
    total = len(results)
    accuracy = correct / total

    print("\n" + "=" * 65)
    print("EMAIL CLASSIFICATION — EVALUATION RESULTS")
    print("=" * 65)
    print(f"\nTest emails:          {total}")
    print(f"Correctly classified: {correct}")
    print(f"Overall Accuracy:     {accuracy:.1%}")

    print("\n--- Per-Class Metrics ---")
    classes = ["interview", "rejected", "applied", "offer"]

    for cls in classes:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)

        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

        print(f"\n  {cls.upper():<12} TP={tp}  FP={fp}  FN={fn}")
        print(f"               Precision={precision:.1%}  Recall={recall:.1%}  F1={f1:.1%}")

    print("\n--- Misclassified ---")
    missed = [r for r in results if not r["correct"]]
    if missed:
        for r in missed:
            print(f"  [{r['expected']} → {r['predicted']}] {r['subject']}")
    else:
        print("  None!")

    return y_true, y_pred

def plot_results(y_true, y_pred):
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        classes = ["interview", "rejected", "applied", "offer"]
        precision_scores, recall_scores, f1_scores = [], [], []

        for cls in classes:
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p == cls)
            fp = sum(1 for t, p in zip(y_true, y_pred) if t != cls and p == cls)
            fn = sum(1 for t, p in zip(y_true, y_pred) if t == cls and p != cls)

            precision = tp / (tp + fp) if (tp + fp) else 0
            recall = tp / (tp + fn) if (tp + fn) else 0
            f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

            precision_scores.append(precision * 100)
            recall_scores.append(recall * 100)
            f1_scores.append(f1 * 100)

        x = np.arange(len(classes))
        width = 0.25

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        #bar chart 
        axes[0].bar(x - width, precision_scores, width, label='Precision')
        axes[0].bar(x, recall_scores, width, label='Recall')
        axes[0].bar(x + width, f1_scores, width, label='F1')

        axes[0].set_xticks(x)
        axes[0].set_xticklabels(classes)
        axes[0].set_ylim(0, 100)
        axes[0].set_title("Per-Class Metrics")
        axes[0].legend()

        #pie chart
        correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        incorrect = len(y_true) - correct

        axes[1].pie(
            [correct, incorrect],
            labels=["Correct", "Incorrect"],
            autopct='%1.1f%%',
            startangle=90
        )
        axes[1].set_title("Overall Accuracy")

        plt.tight_layout()

        # Ensure folder exists
        os.makedirs("evaluation", exist_ok=True)
        path = "evaluation/email_results.png"
        plt.savefig(path)

        print(f"\nGraph saved to: {path}")
        plt.show()

    except ImportError:
        print("\nInstall matplotlib: pip install matplotlib")
        
if __name__ == "__main__":
    y_true, y_pred = run()
    plot_results(y_true, y_pred)
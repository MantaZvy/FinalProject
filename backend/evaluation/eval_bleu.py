#Evaluation 2: BLEU Score for Document Generation. Tests generated resume against synthetic professional references.
import re, os
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

#tokenizer
nltk.download('punkt', quiet=True)

#2 synthetic reference resumes
REFERENCE_1 = """
Alex Carter Computer Science Student Backend Developer
Final year Computer Science student at a UK university
with hands-on experience in backend development API integration and NLP systems.
Proficient in Python JavaScript and React with ability to deliver
efficient scalable solutions in fast-paced environments.
CodeLab Bootcamp Student Developer April 2024 Present
Completed multiple coding workshops specialising in web development
Developed several real-world projects implementing RESTful APIs and frameworks
Earned certifications in web development and software engineering
TalentBridge Agency Administrative Assistant April 2023 April 2024
Managed data tracking systems and internal databases
Coordinated between teams and stakeholders
Supported recruitment processes and candidate evaluation
BSc Computer Science UK University 2022 2026
Skills Python JavaScript TypeScript React Django SQL RESTful APIs Git Bootstrap
"""

REFERENCE_2 = """
Software Developer Candidate
Motivated Computer Science graduate with practical experience in Python development
and full-stack web applications. Strong foundation in backend systems database
management and API design. Proven ability to work collaboratively and deliver quality software.
Team Member NoodleHouse April 2024 Present
Delivered customer service in a high-volume environment
Demonstrated reliability time management and teamwork under pressure
Maintained operational efficiency in fast-paced settings
Administrative Assistant TalentBridge Agency April 2023 April 2024
Utilised data management tools to organise internal workflows
Built professional relationships between stakeholders
Demonstrated analytical and organisational skills
Technical Skills Python JavaScript React SQL FastAPI Git
Education BSc Computer Science 2026
"""

YOUR_GENERATED_RESUME = """
Candidate Name: Alex Carter

Summary:
Dedicated Computer Science student with a strong foundation in Python and JavaScript,
combined with practical experience in customer-facing and administrative roles.
Eager to apply problem-solving skills and technical knowledge in a software development role.

Work Experience:

NoodleHouse, April 2024 - Present | Team Member
- Delivered high-quality customer service in a fast-paced environment
- Collaborated with team members to maintain efficient operations
- Managed multiple tasks under pressure while ensuring service standards
- Maintained a clean and organised workspace

TalentBridge Agency, April 2023 - April 2024 | Administrative Assistant
- Managed internal databases and tracked candidate information
- Assisted in coordinating communication between stakeholders
- Supported recruitment and evaluation processes
- Utilised office tools for daily administrative tasks

Education:
BSc Computer Science, UK University

Skills: Python, JavaScript, React, SQL
"""

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()


#BLEU Evaluation
def run():
    smoothing = SmoothingFunction().method1

    refs = [tokenize(REFERENCE_1), tokenize(REFERENCE_2)]
    hyp = tokenize(YOUR_GENERATED_RESUME)

    b1 = sentence_bleu(refs, hyp, weights=(1, 0, 0, 0), smoothing_function=smoothing)
    b2 = sentence_bleu(refs, hyp, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothing)
    b4 = sentence_bleu(refs, hyp, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothing)

    print("\n" + "=" * 65)
    print("BLEU SCORE EVALUATION — DOCUMENT GENERATION")
    print("=" * 65)

    print(f"\nBLEU-1 (unigram overlap):  {b1:.4f}  ({b1 * 100:.1f}%)")
    print(f"BLEU-2 (bigram overlap):   {b2:.4f}  ({b2 * 100:.1f}%)")
    print(f"BLEU-4 (4-gram fluency):   {b4:.4f}  ({b4 * 100:.1f}%)")

    print("\n--- Interpretation ---")
    print(f"BLEU-1 {'GOOD' if b1 > 0.40 else 'LOW'} — vocabulary overlap")
    print(f"BLEU-2 {'GOOD' if b2 > 0.20 else 'LOW'} — phrase coherence")
    print(f"BLEU-4 {'GOOD' if b4 > 0.10 else 'LOW'} — structural fluency")

    print("\nNote: BLEU scores for resumes are naturally lower than")
    print("machine translation tasks due to multiple valid phrasings.")
    print("=" * 65)

    return b1, b2, b4


def plot_results(b1, b2, b4):
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('BLEU Score Evaluation — Document Generation')

        #chart 1 — BLEU scores
        metrics = ['BLEU-1', 'BLEU-2', 'BLEU-4']
        scores = [b1, b2, b4]

        axes[0].bar(metrics, scores)
        axes[0].set_ylim(0, 0.8)
        axes[0].set_ylabel('Score')
        axes[0].set_title('BLEU Scores')

        for i, score in enumerate(scores):
            axes[0].text(i, score + 0.02, f'{score:.3f}', ha='center')

        #chart 2 — accuracy-style comparison
        thresholds = [0.40, 0.20, 0.10]
        achieved = [b1 * 100, b2 * 100, b4 * 100]
        threshold_pct = [t * 100 for t in thresholds]

        x = range(len(metrics))
        width = 0.35

        axes[1].bar([i - width/2 for i in x], achieved, width, label='Achieved')
        axes[1].bar([i + width/2 for i in x], threshold_pct, width, label='Threshold')

        axes[1].set_xticks(list(x))
        axes[1].set_xticklabels(metrics)
        axes[1].set_ylabel('Score (%)')
        axes[1].set_title('Achieved vs Threshold')
        axes[1].legend()

        plt.tight_layout()

        # Ensure directory exists
        os.makedirs("evaluation", exist_ok=True)
        output_path = "evaluation/bleu_evaluation.png"

        plt.savefig(output_path)
        print(f"\nGraph saved to: {output_path}")

        plt.show()

    except ImportError:
        print("\nInstall matplotlib: pip install matplotlib")

if __name__ == "__main__":
    b1, b2, b4 = run()
    plot_results(b1, b2, b4)

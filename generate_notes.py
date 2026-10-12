
import sys
from google import genai
from google.genai import types

API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are an expert engineering professor and technical academic evaluator for undergraduate engineering (B.Tech) programs.
Transform the provided lecture video into structured, exam-oriented study material aligned with university semester syllabi.
Capture formal definitions, mathematical proofs/derivations, algorithms with Time/Space complexity,
architecture flowcharts/diagrams, and semester exam questions.
"""

NOTE_STRUCTURE_PROMPT = """
Analyze this engineering lecture video and generate comprehensive B.Tech study notes strictly using the following structure:

### 1. 📌 Overview & Problem Statement
- A concise summary (under 150 words) defining the primary engineering challenge or theoretical foundation discussed.

### 2. 📝 Crisp Technical Notes
- **Key Definitions & Terminology:** Bold terms followed by textbook-grade definitions.
- **Working Mechanism & Architecture:** Step-by-step breakdown of how the protocol, algorithm, circuit, or system operates.
- **Formulas, Derivations & Complexity:**
  - Explicit mathematical expressions, boundary conditions, and proofs.
  - Algorithms/Pseudocode with best, average, and worst-case Time & Space complexities (O, Ω, Θ).
- **Comparative Analysis Table:** A clean Markdown table contrasting mechanisms, algorithms, or design trade-offs.

### 3. 🎯 University Semester Exam Questions
- **Short Answer (2–3 Marks / Viva Style):** 3 direct questions focusing on core properties with brief model answers.
- **Long Descriptive / Numerical (5–10 Marks):** 2 standard derivation, numerical, or architecture design questions.

### 4. ⚡ Quick MCQ Self-Test
- 5 GATE/semester-level MCQs (A, B, C, D) testing conceptual edge cases.
- Answer key provided at the end with 1-line rationales.
"""

def main():
    print("=" * 60)
    print("      B.TECH YOUTUBE LECTURE NOTES GENERATOR")
    print("=" * 60)
    
    url = input("\nPaste YouTube Lecture Link: ").strip()
    if not url:
        print("Error: No link provided.")
        input("\nPress Enter to exit...")
        sys.exit()

    print("\n[1/2] Processing video and generating notes with Gemini...")
    print("      (This takes ~30-60 seconds for a full lecture)\n")

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                types.Part.from_uri(
                    file_uri=url,
                    mime_type="video/mp4",
                ),
                types.Part.from_text(text=NOTE_STRUCTURE_PROMPT),
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.25,
            ),
        )

        output_file = "lecture_notes.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print("[2/2] Success! Notes generated.")
        print(f"      Saved to: {output_file}")
        print("=" * 60)

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()
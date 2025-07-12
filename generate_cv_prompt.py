#!/usr/homebrew/bin/env python3
"""
generate_cv_prompt.py
Interactive generator for LaTeX‑CV‑tailoring JSON prompts
"""

import json

# JSON template for generating CV tailoring prompts
TEMPLATE = {
    "instruction": "Revise a LaTeX CV to tailor it to a specific {job_type} job description.",
    "context": {
        "source_file": ".tex source file of the current CV",
        "job_description_file": {
            "filename": "{job_description_filename}",
            "structure": "{job_description_structure}"
        },
        "additional_experience_file": {
            "filename": "{extra_experience_filename}",
            "structure": "{extra_experience_structure}"
        },
        "task": ("Analyze the job description, identify key requirements, and revise the CV to maximise "
                 "alignment with the {job_type} position at the {organization_type}. Highlight relevant "
                 "skills, rephrase experience with appropriate terminology, and remove or condense "
                 "unrelated content. Maintain a professional tone and preserve original structure unless "
                 "clarity or impact would benefit from change.")
    },
    "parameters": {
        "language": "{language}",
        "tone": "{tone}",
        "edits": [
            "emphasize experience aligned with the job description",
            "rewrite descriptions using relevant terminology",
            "summarize or remove low‑relevance content",
            "adjust section ordering for optimal emphasis",
            "incorporate additional content if beneficial",
            "request clarifications if job‑aligned achievements cannot be inferred"
        ],
        "output_format": "{output_format}",
        "preserve": "stylistic and structural consistency unless otherwise specified",
        "constraints": [
            "preserve bibliography/publications section",
            "do not alter macros or layout commands",
            "maintain language unless explicitly changed"
        ],
        "review_mode": "{review_mode}",
        "cv_class": "{cv_class}",
        "target_position_level": "{position_level}",
        "focus_sections": "{focus_sections}",
        "exclude_sections": "{exclude_sections}",
        "integration_mode": "{integration_mode}"
    },
    "examples": []   # Keep or customise as needed
}

def ask(prompt, default=None, split=False):
    # Use print and input separately to mimic raw_input behavior
    if default:
        print(f"{prompt} [{default}]: ", end='', flush=True)
    else:
        print(f"{prompt}: ", end='', flush=True)
    txt = input().strip()
    if not txt and default is not None:
        txt = default
    if split:
        return [i.strip() for i in txt.split(',')] if txt else []
    return txt

# What is the behavior of print statements above when I run this script in a zsh terminal?
# The print statements will display the prompt in the terminal, allowing the user to input their response.
# The `end=''` and `flush=True` ensure that the prompt appears immediately without a newline, and the input is read on the same line.
# Let's try.

def main():
    data = json.loads(json.dumps(TEMPLATE))  # deep copy
    # what does the line above do?
    # It creates a deep copy of the TEMPLATE dictionary to avoid modifying the original template.
    # This allows us to fill in the template with user inputs without altering the original structure.
    # but the script does not use the original TEMPLATE variable after this point?
    # Yes, the script uses the copied data structure to fill in user inputs and generate the final prompt.
    # Is it really necessary to copy the template?
    # Yes, copying the template is necessary to ensure that the original TEMPLATE remains unchanged.
    # So variable 'data' is just a copy of TEMPLATE?
    # Yes, the variable 'data' is a copy of the TEMPLATE dictionary, allowing modifications

    # Basic fields
    job_type = ask("Job type", "industry")
    org_type = ask("Organisation type", "private firm")
    language = ask("Language", "English")
    tone = ask("Tone", "professional")
    out_format = ask("Output format", "annotated LaTeX code block")
    review_mode = ask("Review mode (annotated_suggestions|inline_comments|full_rewrite)", "annotated_suggestions")
    cv_class = ask("LaTeX class", "moderncv")
    pos_level = ask("Position level (intern|junior|mid|senior|postdoc)", "junior")
    focus_sections = ask("Focus sections (comma‑separated)", "work experience,technical skills,projects", split=True)
    exclude_sections = ask("Exclude sections (comma‑separated)", "", split=True)
    integration_mode = ask("Integration mode (add_new_content_to_existing_structure|replace_sections|append_only)",
                           "add_new_content_to_existing_structure")

    # File names / formats
    jd_file = ask("Job‑description filename", "job_description.txt")
    jd_struct = ask("Job‑description structure", "plain text")
    xp_file = ask("Extra‑experience filename", "other_info.json")
    xp_struct = ask("Extra‑experience structure", "nested JSON with sections like education, work experience, skills, etc.")

    # Fill template
    data["instruction"] = data["instruction"].format(job_type=job_type)
    ctx = data["context"]
    ctx["job_description_file"]["filename"] = jd_file
    ctx["job_description_file"]["structure"] = jd_struct
    ctx["additional_experience_file"]["filename"] = xp_file
    ctx["additional_experience_file"]["structure"] = xp_struct
    ctx["task"] = ctx["task"].format(job_type=job_type, organization_type=org_type)

    params = data["parameters"]
    params.update({
        "language": language,
        "tone": tone,
        "output_format": out_format,
        "review_mode": review_mode,
        "cv_class": cv_class,
        "target_position_level": pos_level,
        "focus_sections": focus_sections,
        "exclude_sections": exclude_sections,
        "integration_mode": integration_mode
    })

    # Pretty‑print JSON
    print("\n---- Generated Prompt ----\n")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
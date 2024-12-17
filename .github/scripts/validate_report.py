import re
import sys
import os

# Define the required H2 headings
required_h2_headings = {"解題說明", "程式實作", "效能分析", "測試與驗證", "申論及開發報告"}

# Function to find the report.md file dynamically
def find_report_md(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        if "report.md" in filenames:
            return os.path.join(dirpath, "report.md")
    return None

# Start from the repository root (current script's location)
repo_root = os.path.abspath(os.getcwd())
report_path = find_report_md(repo_root)

# Check if report.md exists
if not report_path or not os.path.isfile(report_path):
    print("::error::report.md not found in the repository.")
    sys.exit(1)

# Read the content of report.md
with open(report_path, "r", encoding="utf-8") as file:
    content = file.read()

# Step 1: Check for the first H1 header as student ID
h1_headers = re.findall(r"^# (.+)", content, re.MULTILINE)

if not h1_headers:
    print(f"::error file={report_path}::The first H1 header is missing (expected Student ID).")
    sys.exit(1)

# Validate that the first H1 looks like a student ID (assuming it's numeric)
student_id = h1_headers[0]
if not re.match(r"^\d+$", student_id):
    print(f"::error file={report_path}::First H1 header '{student_id}' is not a valid Student ID.")
    sys.exit(1)

# Step 2: Check for required H2 headings
found_h2_headings = set(re.findall(r"^## (.+)", content, re.MULTILINE))

# Check for missing H2 headings
missing_headings = required_h2_headings - found_h2_headings
if missing_headings:
    for heading in missing_headings:
        print(f"::error file={report_path}::Missing H2 heading: {heading}")
    sys.exit(1)

print(f"Student ID '{student_id}' detected.")
print("All required H2 headings are present.")

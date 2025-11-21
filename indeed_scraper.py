# --------------------------------------------
# Step 1: Import Libraries
# --------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# --------------------------------------------
# Step 2: Load CSV File
# --------------------------------------------
file_path = "C:/Users/Admin/Desktop/indeed_scraper/sample_jobs_large.csv"  # change if needed

try:
    df = pd.read_csv(file_path)
    print("✅ File loaded successfully!")
except FileNotFoundError:
    print("❌ File not found! Check your file path.")
    exit()

# Preview the data
print("\n📋 Sample data from CSV:\n")
print(df.head())
print("\nColumns available:", list(df.columns))

# --------------------------------------------
# Step 3: Enter filters from user
# --------------------------------------------
job_keyword = input("\nEnter job role keyword (e.g., Python, Data Scientist): ").strip()
location_keyword = input("Enter location keyword (e.g., Pune, Remote): ").strip()

# --------------------------------------------
# Step 4: Filter jobs based on role and location
# --------------------------------------------
mask = pd.Series(True, index=df.index)

# Apply job title filter if given
if job_keyword:
    job_keyword_escaped = re.escape(job_keyword)
    mask &= df['Job Title'].astype(str).str.contains(job_keyword_escaped, case=False, na=False, regex=True)

# Apply location filter if given
if location_keyword:
    location_keyword_escaped = re.escape(location_keyword)
    mask &= df['Location'].astype(str).str.contains(location_keyword_escaped, case=False, na=False, regex=True)

filtered_jobs = df[mask]

# --------------------------------------------
# Step 5: Display & Save Filtered Results
# --------------------------------------------
print(f"\nFound {len(filtered_jobs)} jobs for '{job_keyword or 'Any'}' in '{location_keyword or 'Any'}':\n")

if len(filtered_jobs) > 0:
    print(filtered_jobs.head(10))  # print first 10 only for preview
    base_dir = os.path.dirname(file_path)
    output_file = os.path.join(base_dir, "filtered_sample_jobs.csv")
    filtered_jobs.to_csv(output_file, index=False)
    print(f"\n✅ Saved filtered jobs to: {output_file}")
else:
    print("⚠️ No matching jobs found. File not saved.")

# --------------------------------------------
# Step 6: Check Missing Values
# --------------------------------------------
print("\n🔍 Missing values in each column:")
print(df.isnull().sum())

# --------------------------------------------
# Step 7: Visualization 1 — Top 10 Most Common Job Titles
# --------------------------------------------
plt.figure(figsize=(10,5))
df['Job Title'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Most Common Job Titles")
plt.xlabel("Job Title")
plt.ylabel("Number of Postings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------------------------
# Step 8: Visualization 2 — Job Count by Location (Pie Chart)
# --------------------------------------------
plt.figure(figsize=(8,8))
location_counts = df['Location'].value_counts().head(10)
plt.pie(
    location_counts,
    labels=location_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors
)
plt.title("Top 10 Locations with Most Job Postings (Pie Chart)")
plt.tight_layout()
plt.show()

# --------------------------------------------
# Step 9: Visualization 3 — Average Salary by Job Title
# --------------------------------------------
if 'Salary' in df.columns:
    s = df['Salary'].astype(str).str.replace(',', '')
    s_num = s.str.extract(r'(\d+(?:\.\d+)?)')[0]
    df['Salary_num'] = pd.to_numeric(s_num, errors='coerce')
    
    avg_salary = df.groupby('Job Title')['Salary_num'].mean().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(10,5))
    avg_salary.plot(kind='bar', color='green')
    plt.title("Average Salary by Job Title")
    plt.xlabel("Job Title")
    plt.ylabel("Average Salary (approx)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("\nℹ️ No 'Salary' column found in the dataset.")

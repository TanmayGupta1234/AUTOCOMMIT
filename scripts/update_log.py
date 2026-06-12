#!/usr/bin/env python3
"""
scripts/update_log.py
Generates a daily log entry with a motivational quote, updates repository stats,
and outputs a commit message for the GitHub Actions workflow.
"""

import os
import re
import random
import datetime

# Configuration
LOG_FILE_PATH = os.path.join("data", "daily_log.txt")
README_PATH = "README.md"

# Curated motivational quotes
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "Your time is limited, so don't waste it living someone else's life. - Steve Jobs",
    "The secret of getting ahead is getting started. - Mark Twain",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Keep your face always toward the sunshine - and shadows will fall behind you. - Walt Whitman",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. - Zig Ziglar",
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    "The best way to predict the future is to create it. - Peter Drucker",
    "You miss 100% of the shots you don't take. - Wayne Gretzky",
    "Act as if what you do makes a difference. It does. - William James",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "Quality means doing it right when no one is looking. - Henry Ford",
    "Small daily improvements over time lead to stunning results. - Robin Sharma",
    "Consistency is the key to unlocking your full potential. - Unknown"
]

# Random commit message templates
COMMIT_MESSAGES = [
    "Daily activity update",
    "Repository maintenance",
    "Automated progress update",
    "Keeping contributions active",
    "Timestamp refresh",
    "Daily Update - {date}",
    "Auto Commit #{num}"
]


def get_ist_time():
    """Returns the current time converted to Indian Standard Time (IST)."""
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    return utc_now.astimezone(ist_tz)

def read_commit_count():
    """Parses daily_log.txt to find the count of previous commits."""
    if not os.path.exists(LOG_FILE_PATH):
        return 0
    
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        # Find all occurrences of 'Auto Commit #<num>'
        matches = re.findall(r"Auto Commit #(\d+)", content)
        if matches:
            return max(int(m) for m in matches)
    except Exception as e:
        print(f"Warning: Failed to parse commit count from file: {e}")
    return 0

def update_readme(commit_count, ist_now):
    """Updates the dynamic stats section in README.md."""
    if not os.path.exists(README_PATH):
        print("Warning: README.md not found. Skipping README update.")
        return
    
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = r"<!-- STATS_START -->.*?<!-- STATS_END -->"
        date_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")
        stats_replacement = f"""<!-- STATS_START -->
| Metric | Value |
| :--- | :--- |
| **Total Automated Commits** | `{commit_count}` |
| **Last Successful Run** | `{date_str} IST` |
| **System Status** | `🟢 Operational` |
<!-- STATS_END -->"""
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(pattern, stats_replacement, content, flags=re.DOTALL)
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print("Successfully updated README.md statistics.")
        else:
            print("Warning: Stats placeholder not found in README.md.")
    except Exception as e:
        print(f"Error updating README.md: {e}")

def set_github_output(name, value):
    """Writes variables to GITHUB_OUTPUT environment file for Actions workflow access."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"{name}={value}\n")
            print(f"Set GitHub Actions output: {name}={value}")
        except Exception as e:
            print(f"Error writing to GITHUB_OUTPUT: {e}")
    else:
        print(f"Not running in GitHub Actions environment. Output {name}={value} simulated.")

def main():
    # Ensure data directory exists
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created directory: {log_dir}")
        
    # Get current IST time
    ist_now = get_ist_time()
    date_str = ist_now.strftime("%Y-%m-%d")
    time_str = ist_now.strftime("%H:%M:%S")
    
    # Calculate commit index
    prev_count = read_commit_count()
    current_count = prev_count + 1
    
    # Select a quote and commit message
    quote = random.choice(QUOTES)
    msg_template = random.choice(COMMIT_MESSAGES)
    commit_msg = msg_template.format(date=date_str, num=current_count)
    
    # Build log entry
    log_entry = (
        f"Date: {date_str}\n"
        f"Time: {time_str} IST\n"
        f"Auto Commit #{current_count}\n"
        f"Quote: \"{quote}\"\n"
        f"----------------------------------\n"
    )
    
    # Write to daily log (appends and does not overwrite)
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"Appended log entry for Auto Commit #{current_count} in {LOG_FILE_PATH}")
    
    # Update README statistics
    update_readme(current_count, ist_now)
    
    # Export commit message to GitHub Actions
    set_github_output("commit_message", commit_msg)
    set_github_output("commit_number", str(current_count))
    set_github_output("daily_quote", quote)

if __name__ == "__main__":
    main()

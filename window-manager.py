import pygetwindow as gw
import argparse
import re

# Function to get all open windows
def get_window_titles():
    windows = gw.getAllTitles()
    return [w for w in windows if w.strip()]

# Function to minimize, restore, and focus windows
def toggle_window(window_title, action):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        if action == 'activate':
            if window.isMinimized:
                window.restore()
            window.activate()
        elif action == 'minimize':
            window.minimize()
        return True
    return False

# Function to print windows with numbers
def print_windows(windows, priority_set, priority_patterns):
    for idx, title in enumerate(windows):
        if title in priority_set or any(re.search(p, title) for p in priority_patterns):
            print(f"{idx}: {title}")
        else:
            print(f"{idx}: {title}")

def get_priority_windows(windows, priority_patterns, exclude_patterns):
    priority = []
    others = []
    priority_set = set()

    for w in windows:
        if any(re.search(p, w) for p in priority_patterns) and not any(re.search(ep, w) for ep in exclude_patterns):
            priority.append(w)
            priority_set.add(w)
        else:
            others.append(w)

    return priority + others, priority_set

def handle_priority_windows(priority_patterns, exclude_patterns, action):
    windows = get_window_titles()
    for w in windows:
        if any(re.search(p, w) for p in priority_patterns) and not any(re.search(ep, w) for ep in exclude_patterns):
            toggle_window(w, action)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage and prioritize specific windows.')
    parser.add_argument('--toggl', choices=['activate', 'minimize'], help='Activate or minimize Toggl Track')
    parser.add_argument('--togglplan', choices=['activate', 'minimize'], help='Activate or minimize Toggl Plan')
    parser.add_argument('--tasks', choices=['activate', 'minimize'], help='Activate or minimize Google Calendar Tasks')
    parser.add_argument('--calendar', choices=['activate', 'minimize'], help='Activate or minimize Google Calendar views')
    parser.add_argument('--chatgpt', choices=['activate', 'minimize'], help='Activate or minimize ChatGPT')
    parser.add_argument('--emulator', choices=['activate', 'minimize'], help='Activate or minimize Android Emulator')
    parser.add_argument('--cytracom', choices=['activate', 'minimize'], help='Activate or minimize Cytracom')
    parser.add_argument('--notepad', choices=['activate', 'minimize'], help='Activate or minimize Notepad (Work.txt)')
    parser.add_argument('--outlook', choices=['activate', 'minimize'], help='Activate or minimize Outlook')
    parser.add_argument('--onenote', choices=['activate', 'minimize'], help='Activate or minimize OneNote')
    parser.add_argument('--vscode', choices=['activate', 'minimize'], help='Activate or minimize Visual Studio Code')
    args = parser.parse_args()

    # Define the priority patterns and exclusion patterns based on the arguments
    priority_patterns = []
    exclude_patterns = []

    if args.toggl:
        priority_patterns.append(r"Toggl Track")
        priority_patterns.extend([
            r"Personal - Myself",
            r"Work - Myself",
            r"Work - FamilyBusiness",
            r"Work - Job"
        ])
        handle_priority_windows(priority_patterns, exclude_patterns, args.toggl)
    if args.togglplan:
        priority_patterns.append(r"Toggl Plan - Google Chrome")
        handle_priority_windows(priority_patterns, exclude_patterns, args.togglplan)
    if args.tasks:
        priority_patterns.append(r"Google Calendar - Tasks - Google Chrome")
        handle_priority_windows(priority_patterns, exclude_patterns, args.tasks)
    if args.calendar:
        exclude_patterns.append(r"Google Calendar - Tasks - Google Chrome")
        priority_patterns.extend([
            r"Google Calendar - [A-Za-z]+",  # Matches day-based titles (e.g., Sunday, Monday, etc.)
            r"Google Calendar - 4 days",
            r"Google Calendar - Week",
            r"Google Calendar - Month",
            r"Google Calendar - Year",
            r"Google Calendar - Schedule"
        ])
        handle_priority_windows(priority_patterns, exclude_patterns, args.calendar)
    if args.chatgpt:
        priority_patterns.append(r"ChatGPT — Mozilla Firefox")
        handle_priority_windows(priority_patterns, exclude_patterns, args.chatgpt)
    if args.emulator:
        priority_patterns.append(r"Android Emulator - Brian_Tablet")
        handle_priority_windows(priority_patterns, exclude_patterns, args.emulator)
    if args.cytracom:
        priority_patterns.append(r"Cytracom")
        handle_priority_windows(priority_patterns, exclude_patterns, args.cytracom)
    if args.notepad:
        priority_patterns.append(r"Work.txt - Notepad")
        handle_priority_windows(priority_patterns, exclude_patterns, args.notepad)
    if args.outlook:
        priority_patterns.append(r"Outlook")
        handle_priority_windows(priority_patterns, exclude_patterns, args.outlook)
    if args.onenote:
        priority_patterns.append(r"OneNote")
        handle_priority_windows(priority_patterns, exclude_patterns, args.onenote)
    if args.vscode:
        priority_patterns.append(r"Visual Studio Code")
        handle_priority_windows(priority_patterns, exclude_patterns, args.vscode)

    # If no arguments are provided, list windows and allow selection
    if not any(vars(args).values()):
        while True:
            window_titles = get_window_titles()
            sorted_windows, priority_set = get_priority_windows(window_titles, priority_patterns, exclude_patterns)
            print_windows(sorted_windows, priority_set, priority_patterns)
            try:
                selection = input("Enter window number to minimize/restore (or 'q' to quit): ")
                if selection.lower() == 'q':
                    break
                window_index = int(selection)
                if 0 <= window_index < len(sorted_windows):
                    toggle_window(sorted_windows[window_index], 'activate')
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

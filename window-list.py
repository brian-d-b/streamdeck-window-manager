import pygetwindow as gw

# Function to get all open windows
def get_window_titles():
    windows = gw.getAllTitles()
    return [w for w in windows if w.strip()]

# Function to print windows with numbers
def print_windows(windows):
    for idx, title in enumerate(windows):
        print(f"{idx}: {title}")

if __name__ == "__main__":
    window_titles = get_window_titles()
    print_windows(window_titles)

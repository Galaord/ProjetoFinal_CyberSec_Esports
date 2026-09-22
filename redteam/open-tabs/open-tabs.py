
#!/usr/bin/env python3
"""
open_tabs.py — Open URLs as real browser tabs, each auto-closing after
a set duration, looping forever. Uses Playwright for actual tab control
(webbrowser.open() can't close tabs it opens — this can). 
Usage:
    ./open_tabs.py                          # loop the default URLS list
    ./open_tabs.py url1 url2 url3           # loop these URLs
    ./open_tabs.py -f urls.txt              # loop URLs from a file
    ./open_tabs.py -d 3                     # each tab stays open 3s (default)
    ./open_tabs.py --once                   # go through the list once, then exit
    ./open_tabs.py --headless               # run without a visible window
"""
import argparse
import sys
import time
 
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit(
        "Playwright isn't installed.\n"
        "Try: pip install playwright --break-system-packages && playwright install chromium\n"
        "On NixOS, see the comment at the top of this script for the recommended setup."
    )
 
# Default list of URLs, edit this if you're not passing args/files
URLS = [
    "https://k4talicious.com"
]
 
 
def load_urls_from_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]
 
 
def run(urls: list[str], display_seconds: float, headless: bool, once: bool) -> None:
    if not urls:
        print("No URLs to open.")
        return
 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
 
        try:
            while True:
                for url in urls:
                    page = context.new_page()
                    print(f"Opening {url}")
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    except Exception as e:
                        print(f"  (load issue, closing anyway: {e})")
                    time.sleep(display_seconds)
                    page.close()
                    print(f"Closed {url}")
                if once:
                    break
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            context.close()
            browser.close()
 
 
def main():
    parser = argparse.ArgumentParser(description="Open URLs as tabs that auto-close after N seconds.")
    parser.add_argument("urls", nargs="*", help="URLs to open")
    parser.add_argument("-f", "--file", help="Path to a text file with one URL per line")
    parser.add_argument("-d", "--delay", type=float, default=3.0,
                         help="Seconds each tab stays open before closing (default: 3)")
    parser.add_argument("--once", action="store_true",
                         help="Go through the list once instead of looping forever")
    parser.add_argument("--headless", action="store_true",
                         help="Run without a visible browser window")
    args = parser.parse_args()
 
    if args.file:
        urls = load_urls_from_file(args.file)
    elif args.urls:
        urls = args.urls
    else:
        urls = URLS
 
    run(urls, display_seconds=args.delay, headless=args.headless, once=args.once)
 
 
if __name__ == "__main__":
    main()

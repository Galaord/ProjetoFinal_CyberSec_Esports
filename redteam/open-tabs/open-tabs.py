
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
        "Run inside a Nix shell or install via python3Packages.playwright."
    )

# Default list of URLs
URLS = [
    "https://k4talicious.com"
]


def load_urls_from_file(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def run(
    urls: list[str],
    display_seconds: float,
    headless: bool,
    once: bool,
    batch_size: int,
    repeat_count: int,
) -> None:
    if not urls:
        print("No URLs to open.")
        return

    # Expand the URL list according to repeat_count
    # e.g., ['urlA'] with count=10 becomes ['urlA', 'urlA', ..., 'urlA'] (10 times)
    expanded_urls = []
    for u in urls:
        expanded_urls.extend([u] * repeat_count)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--no-startup-window",
                "--silent-launch",
                "--wm-window-animations-disabled",
            ],
        )
        context = browser.new_context()

        try:
            while True:
                # Chunk expanded URLs into batches of size `batch_size`
                for i in range(0, len(expanded_urls), batch_size):
                    current_batch = expanded_urls[i : i + batch_size]
                    pages = []

                    # 1. Open all tab instances in the current batch
                    print(f"\n--- Opening batch of {len(current_batch)} tab(s) ---")
                    for idx, url in enumerate(current_batch, 1):
                        page = context.new_page()
                        print(f"[{idx}/{len(current_batch)}] Opening {url}")
                        try:
                            page.goto(url, wait_until="domcontentloaded", timeout=15000)
                        except Exception as e:
                            print(f"  (load issue: {e})")
                        pages.append((page, url))

                    # 2. Wait for the set delay while all tabs are open together
                    print(f"Holding {len(pages)} tab(s) open for {display_seconds}s...")
                    time.sleep(display_seconds)

                    # 3. Close all tabs in the batch
                    print(f"Closing batch of {len(pages)} tab(s)...")
                    for page, url in pages:
                        page.close()
                    print(f"Closed all {len(pages)} instance(s).")

                if once:
                    break
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            context.close()
            browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Open URLs as tabs and close them in batches after N seconds."
    )
    parser.add_argument("urls", nargs="*", help="URLs to open")
    parser.add_argument("-f", "--file", help="Path to a text file with one URL per line")
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=3.0,
        help="Seconds tabs stay open before closing the batch (default: 3)",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=10,
        help="Maximum number of tabs per batch (default: 10)",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of duplicate instances to open for each URL (default: 1)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Go through the list once instead of looping forever",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without a visible browser window",
    )
    args = parser.parse_args()

    if args.file:
        urls = load_urls_from_file(args.file)
    elif args.urls:
        urls = args.urls
    else:
        urls = URLS

    run(
        urls,
        display_seconds=args.delay,
        headless=args.headless,
        once=args.once,
        batch_size=args.batch_size,
        repeat_count=args.count,
    )


if __name__ == "__main__":
    main()
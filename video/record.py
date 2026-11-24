import sys, time
sys.path.insert(0, "/home/hatch/.local/lib/python3.12/site-packages")
from playwright.sync_api import sync_playwright

SEGMENTS = [
    ("seg_en", "Please courier the documents to Tuba Pasha, House No. 363, Shahdara, Sukkur, and inform on 03110793467."),
    ("seg_ru", "Assalam o alaikum, mera naam Bilal Ahmed hai, mera mobile number 0301-2345678 hai aur mera CNIC 35202-7654321-3 hai, mujhe apna address update karna hai."),
    ("seg_ur", "اسد شیخ صاحب کی تنخواہ PK78MEZN6535954638337004 میں آتی ہے، شناختی کارڈ 52014-8782700-2 نوٹ کر لیں۔"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/home/hatch/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome",
        args=["--no-sandbox"],
    )
    for name, text in SEGMENTS:
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=f"/home/hatch/workspace/pehchan-guard/video/rec/{name}",
            record_video_size={"width": 1280, "height": 720},
        )
        page = ctx.new_page()
        page.goto("http://127.0.0.1:8765/")
        page.wait_for_timeout(1200)
        page.click("#inp")
        page.keyboard.type(text, delay=28)
        page.wait_for_timeout(900)
        page.click("#go")
        page.wait_for_function(
            "document.querySelector('#meta').textContent.length > 3", timeout=180000
        )
        page.wait_for_timeout(3500)
        ctx.close()
        print("recorded", name, flush=True)
    browser.close()
print("ALL DONE")

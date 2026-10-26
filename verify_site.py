import os
import re
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
html_files.sort()

errors = []

print("=" * 60)
print("1. CHECKING LOCAL LINKS, SRCS, FETCH TARGETS & ANCHORS")
print("=" * 60)

# Build a map of file -> set of IDs
file_ids = {}
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        ids = {el.get('id') for el in soup.find_all(id=True)}
        file_ids[hf] = ids

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check href and src
    links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)
    for link in links:
        if link.startswith(('http://', 'https://', 'mailto:', 'javascript:')):
            continue
        if link.startswith('#'):
            anchor = link[1:]
            if anchor and anchor not in file_ids[hf]:
                errors.append(f"{hf}: Anchor #{anchor} not found in same page")
            continue
        
        parts = link.split('#')
        target_path = parts[0].split('?')[0]
        anchor = parts[1] if len(parts) > 1 else None

        if target_path:
            if not os.path.exists(target_path):
                errors.append(f"{hf}: Referenced file does not exist: {target_path}")
            elif anchor and target_path.endswith('.html'):
                if target_path in file_ids and anchor not in file_ids[target_path]:
                    errors.append(f"{hf}: Anchor #{anchor} not found in target {target_path}")

# Check fetches in script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()
fetch_targets = re.findall(r'fetch\(["\']([^"\']+)["\']\)', js_content)
for ft in fetch_targets:
    if not os.path.exists(ft):
        errors.append(f"script.js: fetch target does not exist: {ft}")

print(f"Checked {len(html_files)} HTML files and script.js.")

print("\n" + "=" * 60)
print("2. CHECKING ZERO TODO, PLACEHOLDER, ALERT IN PUBLIC HTML/JSON")
print("=" * 60)

data_files = [os.path.join('data', f) for f in os.listdir('data') if f.endswith('.json')] if os.path.isdir('data') else []
check_files = html_files + data_files
for cf in check_files:
    with open(cf, 'r', encoding='utf-8') as f:
        text = f.read()
    if 'data-ph' in text:
        errors.append(f"{cf}: Placeholder metric (data-ph) still present, replace with a real number before publishing")
    if 'assets/cv.pdf' in text:
        errors.append(f"{cf}: Stale assets/cv.pdf reference")
    if 'TODO' in text:
        errors.append(f"{cf}: Found 'TODO' in text")
    if 'alert(' in text:
        errors.append(f"{cf}: Found 'alert(' in text")
    if '[TODO:' in text:
        errors.append(f"{cf}: Found '[TODO:' in text")
    if 'placeholder:' in text.lower():
        errors.append(f"{cf}: Found 'placeholder:' in text")

print("\n" + "=" * 60)
print("3. CHECKING HTML VALIDITY (NO DUPLICATE CLOSING TAGS, NO DUPLICATE IDS)")
print("=" * 60)

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if text.count('</html>') != 1:
        errors.append(f"{hf}: Has {text.count('</html>')} </html> closing tags")
    if text.count('</body>') != 1:
        errors.append(f"{hf}: Has {text.count('</body>')} </body> closing tags")

    soup = BeautifulSoup(text, 'html.parser')
    id_list = [el.get('id') for el in soup.find_all(id=True)]
    seen_ids = set()
    for el_id in id_list:
        if el_id in seen_ids:
            errors.append(f"{hf}: Duplicate id '{el_id}'")
        seen_ids.add(el_id)

print("\n" + "=" * 60)
print("4. PLAYWRIGHT BROWSER VERIFICATION (MOBILE & DESKTOP, BRIGHT MODE)")
print("=" * 60)

async def run_browser_tests():
    pages_to_test = [
        'index.html',
        'research.html',
        'projects.html',
        'reading.html',
        'about.html',
        'project-medoptm.html',
        'project-brain-mri.html',
        'project-brainscan-ai.html'
    ]

    cwd = os.path.abspath('.')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for page_name in pages_to_test:
            page_url = f"file://{os.path.join(cwd, page_name)}"
            
            for width in [1280, 375]:
                for theme in ['bright']:
                    context = await browser.new_context(
                        viewport={'width': width, 'height': 800}
                    )
                    page = await context.new_page()

                    console_errors = []
                    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type in ["error"] else None)
                    page.on("pageerror", lambda err: console_errors.append(str(err)))

                    await page.goto(page_url)
                    # Set theme
                    await page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
                    await page.wait_for_timeout(200)

                    # Check overflow
                    overflow = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
                    if overflow:
                        scroll_w = await page.evaluate("() => document.documentElement.scrollWidth")
                        errors.append(f"{page_name} @ {width}px ({theme} mode): Horizontal overflow detected! scrollWidth={scroll_w} > innerWidth={width}")

                    if console_errors:
                        for ce in console_errors:
                            errors.append(f"{page_name} @ {width}px ({theme} mode): Console error: {ce}")

                    await context.close()

        # Test specific interactions on index.html
        print("Testing Interactive Elements on index.html...")
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto(f"file://{os.path.join(cwd, 'index.html')}")

        # 1. Verify Bright Mode & Removal of Dark Mode Controls
        initial_theme = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        if initial_theme != 'bright':
            errors.append(f"Expected default theme 'bright', got '{initial_theme}'")
        dark_btn_count = await page.locator('[data-theme-set="dark"]').count()
        if dark_btn_count > 0:
            errors.append(f"Dark mode button still found in page ({dark_btn_count} instances)")
        dark_mobile_btn = await page.locator('.theme-mobile-btn').count()
        if dark_mobile_btn > 0:
            errors.append(f"Theme mobile button still found in page ({dark_mobile_btn} instances)")

        # 2. Test BibTeX copy button
        copy_btn = page.locator('[data-bibtex-copy]').first
        if await copy_btn.count() > 0:
            await copy_btn.click()
            await page.wait_for_timeout(300)
            toast = page.locator('.toast-feedback')
            toast_count = await toast.count()
            if toast_count == 0:
                errors.append("BibTeX copy failed: toast feedback not shown")

        await context.close()

        # Test Mobile Drawer on 375px
        print("Testing Mobile Drawer on 375px...")
        context = await browser.new_context(viewport={'width': 375, 'height': 700})
        page = await context.new_page()
        await page.goto(f"file://{os.path.join(cwd, 'index.html')}")
        toggle_btn = page.locator('.mobile-toggle')
        drawer = page.locator('.mobile-nav-drawer')
        if await toggle_btn.count() > 0:
            await toggle_btn.click()
            await page.wait_for_timeout(300)
            is_open = await drawer.evaluate("el => el.classList.contains('open')")
            if not is_open:
                errors.append("Mobile drawer failed to open on toggle click")
            
            # Press escape to close
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(300)
            is_open_after = await drawer.evaluate("el => el.classList.contains('open')")
            if is_open_after:
                errors.append("Mobile drawer failed to close on Escape key")

        await context.close()

        # Test Project Filters on projects.html
        print("Testing Project Filters on projects.html...")
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto(f"file://{os.path.join(cwd, 'projects.html')}")
        vlm_btn = page.locator('.filter-btn[data-filter="vlm"]')
        if await vlm_btn.count() > 0:
            await vlm_btn.click()
            await page.wait_for_timeout(200)
            visible_cards = await page.locator('.project-card:visible').count()
            if visible_cards == 0:
                errors.append("Project filter for 'vlm' matched 0 cards")

        await context.close()
        await browser.close()

asyncio.run(run_browser_tests())

print("\n" + "=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for err in errors:
        print("  -", err)
    exit(1)
else:
    print("ALL CHECKS PASSED PERFECTLY! 100% verified.")
    exit(0)


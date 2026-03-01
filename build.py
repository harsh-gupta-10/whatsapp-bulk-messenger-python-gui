"""Build script: converts logo.png -> logo.ico then runs PyInstaller."""
import subprocess
import sys
import os

# Step 1: convert PNG -> ICO
from PIL import Image
img = Image.open("logo.png").convert("RGBA")
img.save("logo.ico", format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print("✓ logo.ico created")

# Step 2: PyInstaller command
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--icon=logo.ico",
    "--name=WA Bulk Messenger",
    # Selenium hidden imports
    "--hidden-import=selenium",
    "--hidden-import=selenium.webdriver",
    "--hidden-import=selenium.webdriver.chrome",
    "--hidden-import=selenium.webdriver.chrome.service",
    "--hidden-import=selenium.webdriver.chrome.options",
    "--hidden-import=selenium.webdriver.common.by",
    "--hidden-import=selenium.webdriver.support.ui",
    "--hidden-import=selenium.webdriver.support.expected_conditions",
    # webdriver-manager hidden imports
    "--hidden-import=webdriver_manager",
    "--hidden-import=webdriver_manager.chrome",
    "--hidden-import=webdriver_manager.core.driver_cache",
    "--hidden-import=webdriver_manager.core.os_manager",
    # Collect all files from these packages
    "--collect-all=selenium",
    "--collect-all=webdriver_manager",
    "ui.py"
]

print("✓ Starting PyInstaller build...")
result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
if result.returncode == 0:
    print("\n✅ Build complete! Exe is in the dist/ folder.")
else:
    print("\n❌ Build failed.")
    sys.exit(1)

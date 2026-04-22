import asyncio
 
import pandas as pd
from playwright.async_api import async_playwright
 
EXCEL_PATH = "challenge.xlsx"
CHALLENGE_URL = "https://rpachallenge.com/"
 
 
def load_data(path: str) -> list[dict]:
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df["Phone Number"] = df["Phone Number"].astype(str)
    return df.to_dict(orient="records")
 
 
async def fill_form(page, row: dict):
    field_map = {
        "First Name":     "First Name",
        "Last Name":      "Last Name",
        "Company Name":   "Company Name",
        "Role in Company":"Role in Company",
        "Address":        "Address",
        "Email":          "Email",
        "Phone Number":   "Phone Number",
    }
 
    for col, label in field_map.items():
        value = str(row.get(col, ""))
 
        input_field = page.locator(
            f"//label[normalize-space(text())='{label}']/following-sibling::input"
        )
        await input_field.fill(value)
 
    await page.locator("input[value='Submit'], button:has-text('Submit')").click()
    await page.wait_for_timeout(300)
 
 
async def main():
    records = load_data(EXCEL_PATH)
 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
 
        await page.goto(CHALLENGE_URL)
        await page.wait_for_load_state("networkidle")
 
        await page.locator("button:has-text('Start')").click()
        await page.wait_for_timeout(500)
 
        for i, row in enumerate(records, 1):
            print(f"Runda {i:2d}/10 → {row['First Name']} {row['Last Name']}")
            await fill_form(page, row)
 
        await page.wait_for_timeout(5000)
        await browser.close()
 
 
if __name__ == "__main__":
    asyncio.run(main())
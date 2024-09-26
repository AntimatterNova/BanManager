import puppeteer from "puppeteer";

async function checkInstagramAccountStatus(username) {
  // Launch browser with custom window size
  const browser = await puppeteer.launch({
    headless: false, // Set to 'false' to see the browser window, or 'true' for headless mode
    args: ['--window-size=500,400'], // Set window size to 800x600
    defaultViewport: null // Disable viewport restrictions so it matches the window size
  });

  const page = await browser.newPage();

  // Optionally, you can set the viewport to match the window size
  await page.setViewport({
    width: 400,
    height: 300,
  });

  try {
    await page.goto(`https://www.instagram.com/${username}/`, {
      waitUntil: "networkidle2",
    });

    await page.waitForSelector("span.x1lliihq", { timeout: 3000 });

    const status = await page.evaluate(() => {
      const accountStat = document.querySelector("span.x1lliihq");
      if (accountStat && accountStat.innerText.includes("Sorry, this page isn't available.")) {
        return "The account is either banned or does not exist.";
      }
      return "The account is active.";
    });

    console.log(status);
  } catch (error) {
    console.error("Error accessing Instagram:", error);
  } finally {
    await browser.close();
  }
}

const username = process.argv[2]; // Get username from command line arguments
checkInstagramAccountStatus(username);

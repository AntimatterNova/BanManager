import puppeteer from "puppeteer";

async function checkInstagramAccountStatus(username) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto(`https://www.instagram.com/${username}/`, {
      waitUntil: "networkidle2",
    });

    await page.waitForSelector("span.x1lliihq", { timeout: 7000 });

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

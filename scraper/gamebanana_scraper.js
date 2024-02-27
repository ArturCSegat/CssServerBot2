import puppeteer from 'puppeteer';

const scroll = async (page, css_s) => {
    await page.evaluate((css_s) => {
        document.querySelector(css_s).scrollIntoView()
    }, css_s);
}

(async () => {
    // Launch the browser and open a new blank page
    const browser = await puppeteer.launch({headless:true});
    const page = await browser.newPage();
    const name = process.argv[2]

    // Navigate the page to a URL
    await page.goto('https://gamebanana.com/search?_sModelName=Mod&_sOrder=date&_idGameRow=2&_sSearchString=' + name, {waitUntil:'domcontentloaded', timeout:0});
    await page.setViewport({width: 1080, height: 1024});

    await new Promise(resolve => setTimeout(resolve, 4000));

    // Wait and click on first result
    const selector = '#SearchResults';
    await scroll(page, selector)
    await page.waitForSelector(selector);

    const click_selector = "#SearchResults > div.Flow > div.RecordsGrid > div:nth-child(1) > div.Identifiers.Cluster > a"
    await page.click(click_selector)
    
    const download_selector = "div.DownloadOptions > a.GreenColor"

    await new Promise(resolve => setTimeout(resolve, 5000));
    await scroll(page, download_selector)
    await page.waitForSelector(download_selector)
    // https://gamebanana.com/mods/download/123880#FileInfo_360449
    const [download_link, map_name] = await page.evaluate((download_selector) => {
        const link = document.querySelector(download_selector).href
        const info = link.split('#')[1]
        const id = info.split('_')[1]
        return ["https://gamebanana.com/dl/" + id, document.getElementById("PageTitle").innerText.split('\n')[0]]
    }, download_selector)
    
    console.log(map_name)
    console.log(page.url())
    console.log(download_link)
    await browser.close()
})();

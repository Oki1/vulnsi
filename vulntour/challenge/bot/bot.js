const puppeteer = require('puppeteer-core');

const TARGET_URL = (process.env.TARGET_URL || 'http://web:8000').replace(/\/+$/, '');
const FLAG = process.env.FLAG || 'dctf{part1_part2_part3_part4}';
const POLL_MS = 5000;

function flagPart(flag, index) {
    const size = Math.floor(flag.length / 4);
    const parts = [flag.slice(0, size), flag.slice(size, 2 * size), flag.slice(2 * size, 3 * size), flag.slice(3 * size)];
    return parts[index];
}

const cookieValue = flagPart(FLAG, 1);
const cookieHost = new URL(TARGET_URL).hostname;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function visit(target) {
    let browser;
    try {
        browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium',
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
        });
        const page = await browser.newPage();
        await page.setCookie({
            name: 'flag_part2',
            value: cookieValue,
            domain: cookieHost,
            path: '/',
            httpOnly: false,
            secure: false,
        });
        const destination = new URL(target, TARGET_URL);
        const finalUrl = TARGET_URL + destination.pathname + destination.search;
        console.log('visiting', finalUrl);
        await page.goto(finalUrl, { waitUntil: 'networkidle2', timeout: 20000 });
        await sleep(1500);
    } catch (error) {
        console.error('visit error', error.message);
    } finally {
        if (browser) await browser.close();
    }
}

async function run() {
    console.log('bot started, target', TARGET_URL);
    while (true) {
        try {
            const response = await fetch(TARGET_URL + '/bot/queue');
            const items = await response.json();
            for (const item of items) {
                await visit(item);
            }
        } catch (error) {
            console.error('poll error', error.message);
        }
        await sleep(POLL_MS);
    }
}

run();

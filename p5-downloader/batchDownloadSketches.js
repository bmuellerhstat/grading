// npm install puppeteer node-fetch fs path
// node batchDownloadSketches.js

const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const fetch = require("node-fetch");

const urls = `
https://editor.p5js.org/username1/sketches/projectid1
https://editor.p5js.org/username2/sketches/projectid2
`.trim().split("\n"); // Paste URLs here

async function downloadSketch(username, projectName) {
    const url = `https://editor.p5js.org/${username}/sketches/${projectName}`;

    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    let projectJson = null;

    page.on("response", async (response) => {
        try {
            const reqUrl = response.url();
            if (reqUrl.includes(`/editor/${username}/projects/${projectName}`)) {
                const json = await response.json();
                if (json.project && json.project.files) {
                    projectJson = json.project;
                } else if (json.files) {
                    projectJson = json;
                }
            }
        } catch (e) { }
    });

    console.log(`🌐 Loading: ${url}`);
    await page.goto(url, { waitUntil: "networkidle0" });
    await new Promise(resolve => setTimeout(resolve, 5000));

    if (!projectJson) {
        console.error(`❌ Could not retrieve project JSON for ${username}/${projectName}`);
        await browser.close();
        return;
    }

    const folderName = `downloads/${username}_${projectName}`;
    fs.mkdirSync(folderName, { recursive: true });

    for (const file of projectJson.files || projectJson.project.files || []) {
        const filePath = path.join(folderName, file.name);

        if (file.content) {
            fs.writeFileSync(filePath, file.content, "utf-8");
            console.log(`✅ Saved text file: ${file.name}`);
        } else if (file.url) {
            const res = await fetch(file.url);
            const buffer = await res.buffer();
            fs.writeFileSync(filePath, buffer);
            console.log(`✅ Downloaded binary file: ${file.name}`);
        } else {
            console.warn(`⚠️ Skipping file "${file.name}" (no content or URL).`);
        }
    }

    await browser.close();
    console.log(`✅ Done with ${username}/${projectName}\n`);
}

(async () => {
    for (const fullUrl of urls) {
        const match = fullUrl.match(/p5js\.org\/([^\/]+)\/sketches\/([^\/]+)/);
        if (match) {
            const [, username, projectName] = match;
            await downloadSketch(username, projectName);
        } else {
            console.warn(`⚠️ Invalid URL format: ${fullUrl}`);
        }
    }
})();

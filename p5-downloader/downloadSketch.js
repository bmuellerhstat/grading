// npm install puppeteer node-fetch fs path
// node downloadSketch.js

const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const fetch = require("node-fetch"); // ← correctly import fetch

(async () => {
    const username = "username1";
    const projectName = "projectid1";
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

    await page.goto(url, { waitUntil: "networkidle0" });
    await new Promise(resolve => setTimeout(resolve, 5000));

    if (!projectJson) {
        console.error("❌ Error: Project JSON not found in network responses.");
        await browser.close();
        process.exit(1);
    }

    const folderName = `downloads/${username}_${projectName}`;
    fs.mkdirSync(folderName, { recursive: true });

    const textFileTypes = new Set(["javascript", "html", "css"]);

    for (const file of projectJson.files || projectJson.project.files || []) {
        const filePath = path.join(folderName, file.name);


        if (file.content) {
            // 📝 Save text-based files
            fs.writeFileSync(filePath, file.content, "utf-8");
            console.log(`✅ Saved text file: ${file.name}`);
        } else if (file.url) {
            // 💾 Download binary files
            const res = await fetch(file.url);
            const buffer = await res.buffer();
            fs.writeFileSync(filePath, buffer);
            console.log(`✅ Downloaded binary file: ${file.name}`);
        } else {
            console.warn(`⚠️ Skipping file "${file.name}" (no content or URL).`);
        }
    }

    await browser.close();
})();







// downloadSketch.js

// const fs = require("fs");
// const path = require("path");
// const puppeteer = require("puppeteer");
// const fetch = require("node-fetch");

// // === CONFIGURATION ===
// // Replace this with your sketch URL:
// const SKETCH_URL = "https://editor.p5js.org/editor/tejasbobbili/projects/eFE3fFPMu";

// // Output directory
// const OUTPUT_DIR = path.join(__dirname, "downloaded_sketch");

// async function fetchSketchJson(page) {
//   return await page.evaluate(() => {
//     return window.__NEXT_DATA__.props.pageProps.project;
//   });
// }

// async function saveProjectFiles(project, outputDir) {
//   if (!fs.existsSync(outputDir)) {
//     fs.mkdirSync(outputDir);
//   }

//   for (const file of project.files || []) {
//     const filePath = path.join(outputDir, file.name);

//     if (file.content) {
//       // Save text-based files (e.g., .js, .html, .css)
//       fs.writeFileSync(filePath, file.content, "utf-8");
//       console.log(`✅ Saved text file: ${file.name}`);
//     } else if (file.url) {
//       try {
//         const res = await fetch(file.url);
//         if (!res.ok) throw new Error(`Failed to fetch ${file.name}`);
//         const buffer = await res.buffer();
//         fs.writeFileSync(filePath, buffer);
//         console.log(`✅ Downloaded binary file: ${file.name}`);
//       } catch (err) {
//         console.error(`❌ Failed to download "${file.name}": ${err.message}`);
//       }
//     } else {
//       console.warn(`⚠️ Skipping file "${file.name}" (no content or URL).`);
//     }
//   }
// }

// async function main() {
//   const browser = await puppeteer.launch({ headless: "new" });
//   const page = await browser.newPage();
//   console.log(`🌐 Opening sketch: ${SKETCH_URL}`);
//   await page.goto(SKETCH_URL, { waitUntil: "networkidle0" });

//   console.log("📦 Extracting sketch JSON...");
//   const project = await fetchSketchJson(page);

//   console.log("💾 Saving files...");
//   await saveProjectFiles(project, OUTPUT_DIR);

//   await browser.close();
//   console.log("✅ Done.");
// }

// main().catch((err) => {
//   console.error("🚨 Error:", err);
// });

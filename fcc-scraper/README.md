# How to run the API?

- cd into `fcc-scraper`
- Make sure that node modules are installed, `npm install i`

For a single file:
```bash
node index.js sep10info.json
```

For multiple files:
```bash
node index.js sep10info.json sep11info.json
```

This will write to two identical files, for example:
* `sep11data.csv` for consistent loading into dashboard
* `sep11data2411151234.csv` for archive purposes
# How to run the API?

- cd into `fcc-scraper`
- Make sure that node modules are installed, `npm install i`
- Run the command `node index.js`

# How to test the api locally?

```
curl "http://localhost:3000/?filePath=sep10info.json"
curl "http://localhost:3000/?filePath=sep11info.json"
```

This will write to two identical files, for example:
* `sep11data.csv` for consistent loading into dashboard
* `sep11data2411151234.csv` for archive purposes
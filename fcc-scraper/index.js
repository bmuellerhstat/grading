const fs = require("fs");
const path = require("path");

function getCurrentTimestamp() {
  const now = new Date();
  const year = String(now.getFullYear()).slice(-2);
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hour = String(now.getHours()).padStart(2, '0');
  const minute = String(now.getMinutes()).padStart(2, '0');
  return `${year}${month}${day}${hour}${minute}`;
}

function processFile(filePath) {
  try {
    const getPath = path.resolve(filePath);
    const content = fs.readFileSync(getPath);
    const data = JSON.parse(content);
    const sepYear = filePath.substring(0, 5);  // e.g., "sep10" or "sep11"

    // Create archive folder for the specific sepYear if it doesn't exist
    const sepYearArchiveDir = path.join(__dirname, `${sepYear}archive`);
    if (!fs.existsSync(sepYearArchiveDir)) {
      fs.mkdirSync(sepYearArchiveDir);
    }

    // Define paths for timestamped and static files
    const outputFile = path.join(sepYearArchiveDir, `${sepYear}data${getCurrentTimestamp()}.csv`);
    const staticFile = `${sepYear}data.csv`;

    const lessons = ["Username"];
    data.assignments.forEach((a) => {
      a.lessons.forEach((b) => {
        lessons.push(b.title);
      });
    });
    lessons.push("Total");

    const headers = lessons.join(",") + "\n";
    fs.writeFileSync(outputFile, headers);
    fs.writeFileSync(staticFile, headers);
    console.log(`Files created: ${outputFile}, ${staticFile}`);

    data.students.forEach((student) => {
      getCompletedLessons(student, data.assignments, lessons, outputFile, staticFile);
    });
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
  }
}

async function getCompletedLessons(username, lessons, lessonHeaders, outputFile, staticFile) {
  try {
    const response = await fetch(
      `https://api.freecodecamp.org/api/users/get-public-profile?username=${username}`
    );
    const result = await response.json();
    if (result.entities) {
      const challenges = result.entities.user[username].completedChallenges;
      handleSearch(challenges, lessons, username, lessonHeaders, outputFile, staticFile);
    }
  } catch (error) {
    console.error(`Error fetching data for ${username}:`, error);
  }
}

function handleSearch(fcChallenges, lessons, username, lessonHeaders, outputFile, staticFile) {
  const completedLessons = [];
  lessons.forEach((chunk) => {
    chunk.lessons.forEach((lesson) => {
      if (fcChallenges.some((challenge) => challenge.id == lesson.id)) {
        completedLessons.push(lesson.title);
      }
    });
  });
  handleWrite(completedLessons, username, lessonHeaders, outputFile, staticFile);
}

function handleWrite(data, user, lessonHeaders, outputFile, staticFile) {
  const payload = [user];
  let total = 0;

  lessonHeaders.forEach((header, index) => {
    if (index > 0 && index < lessonHeaders.length - 1) {
      payload.push(data.includes(header) ? 1 : 0);
    }
  });

  total = payload.slice(1).reduce((sum, val) => sum + val, 0);
  payload.push(total);

  const row = payload.join(",") + "\n";
  fs.appendFileSync(outputFile, row);
  fs.appendFileSync(staticFile, row);
  console.log(`Appended data for ${user} to files: ${outputFile}, ${staticFile}`);
}

// Entry point
const filePaths = process.argv.slice(2);
if (filePaths.length === 0) {
  console.error("Please specify at least one JSON file path to process.");
  process.exit(1);
}

filePaths.forEach(processFile);

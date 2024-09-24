const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(cors());

const csvFilePath = path.join(__dirname, "data.csv");

async function getCompletedAssignments(username) {
  const [getStudent, getMeta] = await Promise.all([
    fetch(
      `https://api.freecodecamp.org/api/users/get-public-profile?username=${username}`
    ),
    fetch(
      "https://raw.githubusercontent.com/freeCodeCamp/freeCodeCamp/main/curriculum/challenges/_meta/basic-javascript/meta.json"
    ),
  ]);

  const [student, meta] = await Promise.all([
    getStudent.json(),
    getMeta.json(),
  ]);

  const challengesMap = meta.challengeOrder.reduce((map, challenge) => {
    map[challenge.id] = challenge.title;
    return map;
  }, {});

  const completedChallenges = student.entities.user[
    username
  ].completedChallenges.map((challenge) => {
    challenge.completedDate = new Date(
      challenge.completedDate
    ).toLocaleDateString();
    if (challengesMap[challenge.id]) {
      challenge.title = challengesMap[challenge.id];
    }
    return challenge;
  });

  return [completedChallenges, meta.challengeOrder];
}

function createCSVIfNotExists(challengeOrder) {
  if (!fs.existsSync(csvFilePath)) {
    const headers = [
      "username",
      ...challengeOrder.map((challenge) => challenge.title),
      "completion rate",
    ];
    fs.writeFileSync(csvFilePath, headers.join(",") + "\n");
  }
}

function appendStudentToCSV(username, completedChallenges, challengeOrder) {
  const completedTitles = completedChallenges.map(
    (challenge) => challenge.title
  );
  const row = [username];
  let totalCompleted = 0;

  challengeOrder.forEach((challenge) => {
    if (completedTitles.includes(challenge.title)) {
      row.push("1");
      totalCompleted += 1;
    } else {
      row.push("0");
    }
  });

  const totalChallenges = challengeOrder.length;
  const completionRate = `${totalCompleted} / ${totalChallenges}`;
  row.push(completionRate);

  fs.appendFileSync(csvFilePath, row.join(",") + "\n");
}

function studentExistsInCSV(username) {
  if (fs.existsSync(csvFilePath)) {
    const csvData = fs.readFileSync(csvFilePath, "utf8");
    return csvData.split("\n").some((row) => row.startsWith(username));
  }
  return false;
}

app.get("/", (req, res) => {
  const { student } = req.query;

  if (!student) {
    return res
      .status(400)
      .json({ error: 'The "student" query parameter is required!' });
  }

  getCompletedAssignments(student)
    .then(([completedChallenges, challengeOrder]) => {
      createCSVIfNotExists(challengeOrder);

      if (!studentExistsInCSV(student)) {
        appendStudentToCSV(student, completedChallenges, challengeOrder);
      }

      res.json({ status: "Done!" });
    })
    .catch((err) => {
      res.status(500).json({ error: "Something went wrong!", details: err });
    });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

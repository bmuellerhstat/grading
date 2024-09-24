const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());

async function getCompletedAssignments(username) {
  // Fetch in parallel for faster speeds
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

  // Convert to map
  const challengesMap = meta.challengeOrder.reduce((map, challenge) => {
    map[challenge.id] = challenge.title;
    return map;
  }, {});

  const completedChallenges = student.entities.user[
    username
  ].completedChallenges.map((challenge) => {
    // Replace timecode with formatted time
    challenge.completedDate = new Date(
      challenge.completedDate
    ).toLocaleDateString();

    // Set the title of challenge using challengeMap title
    if (challengesMap[challenge.id]) {
      challenge.title = challengesMap[challenge.id];
    }

    return challenge;
  });

  return [completedChallenges, meta.challengeOrder];
}

app.get("/", (req, res) => {
  const { student } = req.query;

  if (!student) {
    return res
      .status(400)
      .json({ error: 'The "student" query parameter is required!' });
  }

  getCompletedAssignments(student)
    .then((completedAssignments) => {
      res.json({
        student: student,
        challenges: completedAssignments[0],
        meta: completedAssignments[1],
      });
    })
    .catch((err) => {
      res.status(500).json({ error: "Something went wrong!", details: err });
    });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

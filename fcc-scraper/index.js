const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();

app.use(express.json());
app.use(cors());

app.get("/", (req, res) => {
  const { filePath } = req.query;
  if (!filePath) {
    return res.status(400).json({ error: "Must supply json file path!" });
  }

  try {
    const getPath = path.resolve(filePath);
    const content = fs.readFileSync(getPath);
    const data = JSON.parse(content);

    const lessons = [];
    lessons.push("Username");
    data.assignments.forEach((a) => {
      a.lessons.forEach((b) => {
        lessons.push(b.title);
      });
    });
    lessons.push("Total");

    fs.writeFile("output.csv", lessons.join(",") + "\n", (err) => {
      if (err) {
        console.error("Error writing to file", err);
      } else {
        console.log("File created and headers written successfully");
      }
    });

    // Process each student and fetch their completed lessons
    data.students.forEach((i) => {
      getCompletedLessons(i, data.assignments, lessons);
    });
  } catch (error) {
    console.error(error);
  }
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something broke!");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

async function getCompletedLessons(username, lessons, lessonHeaders) {
  try {
    const response = await fetch(
      `https://api.freecodecamp.org/api/users/get-public-profile?username=${username}`
    );
    const result = await response.json();
    if (result.entities != null) {
      const challenges = result.entities.user[username].completedChallenges;
      handleSearch(challenges, lessons, username, lessonHeaders);
    }
  } catch (error) {
    console.error(error);
  }
}

function handleSearch(fcChallenges, lessons, username, lessonHeaders) {
  const completedLessons = [];

  //get completed lessons
  lessons.forEach((chunk) => {
    chunk.lessons.forEach((lesson) => {
      const isCompleted = fcChallenges.find(
        (challenge) => challenge.id == lesson.id
      );
      if (isCompleted) {
        completedLessons.push(lesson.title);
      }
    });
  });

  hanldeWrite(completedLessons, username, lessonHeaders.join(","));
}

function hanldeWrite(data, user, line1) {
  const payload = [];
  let total = 0;

  payload.push(user);

  line1.split(",").forEach((i, index) => {
    if (index != 0 && index != line1.split(",").length) {
      if (data.includes(i)) {
        payload.push(1); //Did lesson
      } else {
        payload.push(0); //Did not do lesson
      }
    }
  });

  //calc total lessons completed by each student
  payload.forEach((a, index) => {
    if (index != 0) {
      total += parseInt(a);
    }
  });

  payload.push(total);

  fs.appendFile("output.csv", payload.join(",") + "\n", (err) => {
    if (err) {
      console.error("Error appending to file", err);
    } else {
      console.log("Content appended successfully");
    }
  });
}

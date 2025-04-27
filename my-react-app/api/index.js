const express = require("express");
const { spawn } = require("child_process");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

app.post("/check-grammar", (req, res) => {
  const input = req.body.input;

  // Gọi script Python với input
  const pythonProcess = spawn("python3", ["grammar_checker.py", input]);

  let result = "";
  let error = "";

  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    error += data.toString();
  });

  pythonProcess.on("close", (code) => {
    if (code === 0) {
      try {
        const parsedResult = JSON.parse(result);
        res.json({ success: true, result: parsedResult });
      } catch (e) {
        res
          .status(500)
          .json({ success: false, error: "Invalid response from Python" });
      }
    } else {
      res.status(500).json({ success: false, error });
    }
  });
});

app.listen(3000, () => console.log("Server running on port 3000"));

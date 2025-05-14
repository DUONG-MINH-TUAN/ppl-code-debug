const express = require("express");
const { spawn } = require("child_process");
const path = require("path"); // Thêm module path để xử lý đường dẫn
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

app.post("/check-grammar", (req, res) => {
  const input = req.body.input;

  const pythonScriptPath = path.join(
    __dirname,
    "..",
    "..",
    "Grammar-rules-checking",
    "grammarRules",
    "run.py"
  );

  const pythonProcess = spawn("py", [pythonScriptPath, input]);
  // Gọi script Python với đường dẫn chính xác
  // const pythonProcess = spawn("py", [pythonScriptPath, input]);

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
      res
        .status(500)
        .json({ success: false, error: error || "Python execution failed" });
    }
  });
});

app.listen(3000, () => console.log("Server running on port 3000"));

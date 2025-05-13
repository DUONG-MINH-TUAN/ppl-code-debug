const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const cors = require("cors");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Định nghĩa đường dẫn đến run.py
const pythonScriptPath = path.join(
  __dirname,
  "..",
  "..",
  "Grammar-rules-checking",
  "grammarRules",
  "run.py"
);

// Debug đường dẫn
console.log("Python script path:", pythonScriptPath);

// Endpoint để kiểm tra ngữ pháp
app.post("/check-grammar", (req, res) => {
  const input = req.body.input;

  // Kiểm tra nếu input không được cung cấp
  if (!input) {
    return res.status(400).json({ success: false, error: "Input is required" });
  }

  // Chạy script Python
  const pythonProcess = spawn("py", [`"${pythonScriptPath}"`, "test", input], {
    shell: true,
  });

  let result = "";
  let error = "";

  // Lấy dữ liệu từ stdout
  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  // Lấy dữ liệu từ stderr
  pythonProcess.stderr.on("data", (data) => {
    error += data.toString();
  });

  // Xử lý khi quá trình Python kết thúc
  pythonProcess.on("close", (code) => {
    if (code === 0) {
      try {
        // Tách kết quả JSON từ output
        const jsonStart = result.indexOf("{");
        const jsonEnd = result.lastIndexOf("}") + 1;
        const jsonString = result.slice(jsonStart, jsonEnd);
        const parsedResult = JSON.parse(jsonString);
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

  // Xử lý lỗi khi spawn thất bại
  pythonProcess.on("error", (err) => {
    res.status(500).json({
      success: false,
      error: `Failed to start Python process: ${err.message}`,
    });
  });
});

// Khởi động server
app.listen(3000, () => console.log("Server running on port 3000"));

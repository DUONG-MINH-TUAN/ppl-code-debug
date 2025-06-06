const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

const pythonScriptPath = path.join(
  __dirname,
  "..",
  "..",
  "Grammar-rules-checking",
  "grammarRules",
  "run.py"
);

console.log("Python script path:", pythonScriptPath);

app.post("/check-grammar", (req, res) => {
  const input = req.body.input;

  // Kiểm tra nếu input không được cung cấp
  if (!input) {
    return res.status(400).json({ success: false, error: "Input is required" });
  }

  // Chuẩn hóa input: chỉ thay thế ký tự xuống dòng, giữ nguyên khoảng trắng giữa các từ
  const normalizedInput = input
    .replace(/(\r\n|\n|\r)/g, " ") // Thay xuống dòng bằng khoảng trắng
    .trim(); // Loại bỏ khoảng trắng thừa ở đầu và cuối

  // Chạy script Python
  const pythonProcess = spawn("py", [`"${pythonScriptPath}"`, "test"], {
    shell: true,
  });

  // Gửi input qua stdin
  pythonProcess.stdin.write(normalizedInput);
  pythonProcess.stdin.end();

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
    console.log("Python stdout:", result); // Debug output
    console.log("Python stderr:", error); // Debug error

    if (code === 0) {
      try {
        const cleanedResult = result.trim();
        if (!cleanedResult) {
          throw new Error("Empty response from Python");
        }
        const parsedResult = JSON.parse(cleanedResult);
        res.json({ success: true, result: parsedResult });
      } catch (e) {
        res.status(500).json({
          success: false,
          error: "Invalid response from Python",
          details: e.message,
          stdout: result,
          stderr: error,
        });
      }
    } else {
      res.status(500).json({
        success: false,
        error: "Python execution failed",
        stdout: result,
        stderr: error,
      });
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

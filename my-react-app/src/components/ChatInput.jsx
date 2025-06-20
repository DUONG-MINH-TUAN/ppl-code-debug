import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "../styles/ChatInput.css";

function ChatInput({ onSendMessage }) {
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState(null);

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      const maxHeight = 200;
      const newHeight = Math.min(textarea.scrollHeight, maxHeight);
      textarea.style.height = newHeight + "px";
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  // const checkGrammar = async (code, callback) => {
  //   try {
  //     const response = await axios.post("http://localhost:3000/check-grammar", {
  //       input: code,
  //     });
  //     setResult(response.data);

  //     if (!response.data.success) {
  //       console.error("Grammar check failed:", response.data.error);
  //       const errorMessage = response.data.error;
  //       toast.error(errorMessage, {
  //         position: "top-center",
  //         autoClose: 5000,
  //         hideProgressBar: false,
  //         closeOnClick: true,
  //         pauseOnHover: true,
  //         draggable: true,
  //       });
  //       // Pass error message to ChatContainer
  //       callback(errorMessage, "error");
  //     } else if (!response.data.result.success) {
  //       console.error("Invalid syntax:", response.data.result.errors);
  //       const errorMessages = response.data.result.errors;
  //       errorMessages.forEach((error) => {
  //         toast.error(error, {
  //           position: "top-center",
  //           autoClose: 5000,
  //           hideProgressBar: false,
  //           closeOnClick: true,
  //           pauseOnHover: true,
  //           draggable: true,
  //         });
  //       });
  //       // Pass combined error messages to ChatContainer
  //       const combinedErrors = errorMessages.join(", ");
  //       callback(combinedErrors, "error");
  //     } else {
  //       const successMessage = response.data.result.message;
  //       toast.success(successMessage, {
  //         position: "top-center",
  //         autoClose: 5000,
  //         hideProgressBar: false,
  //         closeOnClick: true,
  //         pauseOnHover: true,
  //         draggable: true,
  //       });
  //       // Pass success message to ChatContainer
  //       callback(successMessage, "success");
  //     }
  //   } catch (error) {
  //     setResult({ success: false, error: "Server error" });
  //     console.error("Error calling grammar check API:", error.message);
  //     const errorMessage = "Server error: " + error.message;
  //     toast.error(errorMessage, {
  //       position: "top-center",
  //       autoClose: 5000,
  //       hideProgressBar: false,
  //       closeOnClick: true,
  //       pauseOnHover: true,
  //       draggable: true,
  //     });
  //     // Pass server error to ChatContainer
  //     callback(errorMessage, "error");
  //   }
  // };

  const handleAttachClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      console.log("Selected file(s):", files);
    }
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (inputValue.trim()) {
      console.log("Sending useEffect code:", inputValue);

      onSendMessage(inputValue.trim(), (grammarResponse, type) => {

      });

      // Check grammar with callback
      // checkGrammar(inputValue, (grammarResponse, type) => {
      //   // Grammar check completed, response already sent via onSendMessage
      // });

      setInputValue("");
      setTimeout(adjustTextareaHeight, 0);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <div style={{ width: "100%" }}>
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        closeOnClick
        pauseOnHover
        draggable
      />
      <form className="chat-input-container" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className="chat-input"
          placeholder="Enter code"
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          rows={1}
        />
        <div className="input-actions">
          <button
            type="button"
            className="action-btn attachment"
            onClick={handleAttachClick}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
            </svg>
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: "none" }}
            multiple
          />
          <button
            type="submit"
            className="send-btn"
            disabled={!inputValue.trim()}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="send-icon"
            >
              <path d="M22 2L11 13"></path>
              <path d="M22 2l-7 20-4-9-9-4 20-7z"></path>
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatInput;
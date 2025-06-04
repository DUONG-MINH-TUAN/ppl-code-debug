import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import "../styles/ChatContainer.css";

function ChatContainer({ onFirstMessage }) {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    setIsActive(true); // Kích hoạt khi component mount
  }, []);
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending new messages
  const handleSendMessage = async (message, grammarCallback) => {
    // Add user message to chat
    setMessages((prevMessages) => {
      const newMessages = [...prevMessages, { text: message, isUser: true }];
      console.log("Updated messages after user input:", newMessages);
      return newMessages;
    });

    try {
      const grammarResponse = await axios.post(
        "http://localhost:3000/check-grammar",
        {
          input: message,
        }
      );

      let grammarMessage = "";
      let isError = false;

      if (!grammarResponse.data.success) {
        grammarMessage = grammarResponse.data.error;
        isError = true;
      } else if (!grammarResponse.data.result.success) {
        grammarMessage = grammarResponse.data.result.errors
          .map((err) => `${err.error}\nSuggestion: ${err.suggestion}`)
          .join("\n\n");
        isError = true;
        console.log("Grammar errors:", grammarMessage);
      } else {
        grammarMessage = grammarResponse.data.result.message;
        isError = false;
      }

      setMessages((prevMessages) => {
        const newMessages = [
          ...prevMessages,
          {
            text: grammarMessage,
            isUser: false,
            isError: isError,
          },
        ];
        return newMessages;
      });
    } catch (grammarError) {
      console.error("Error calling grammar check API:", grammarError.message);
      const errorMessage = "Server error: " + grammarError.message;
      setMessages((prevMessages) => {
        const newMessages = [
          ...prevMessages,
          { text: errorMessage, isUser: false, isError: true },
        ];
        console.log("Updated messages after error:", newMessages);
        return newMessages;
      });
    }
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className={`chat-section ${isActive ? "active" : ""}`}>
      {" "}
      <div className="chat-messages">
        {messages.length > 0 ? (
          messages.map((message, index) => {
            return (
              <ChatMessage
                key={index + message.text}
                message={message.text}
                isUser={message.isUser}
                isError={message.isError}
              />
            );
          })
        ) : (
          <div className="chat-messages">No messages yet</div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-wrapper">
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}

export default ChatContainer;

import React, { useState } from "react";

const QuestionMessage = (props) => {
  return (
      <div className="chatbox">
        <div className="chat chat-end mt-2 ml-2">
          <div className="chat-bubble whitespace-normal">
            {props.currentQuestion}
          </div>
          <div className="chat chat-start ml-2 w-3/4">
            <div className="chat-bubble whitespace-normal">{props.message}</div>
          </div>
        </div>
      </div>
    )
};
export default QuestionMessage;

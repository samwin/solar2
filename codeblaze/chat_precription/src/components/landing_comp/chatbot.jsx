import React from "react";
import Message from "./message";
import {
  BsAppIndicator,
  BsCollectionPlay,
  BsFillSendFill,
} from "react-icons/bs";
import { useState, useRef } from "react";
import MapModal from "./MapModal";
import { SiGooglemaps } from "react-icons/si";
import QuestionMessage from "./questionMessage";

function Chatbox(props) {
  const [value, setValue] = useState("");
  const [chats, setChats] = useState([]);
  const [isMapModalOpen, setMapModalOpen] = useState(false);
  const [image, setImage] = useState();
  const dialog = useRef();
  const answers = [];
  const appendItem = (newItem) => {
    setChats((preItem) => [...preItem, newItem]);

    console.log(chats);
  };
  const clearChat = () => {
    setChats([]);
    setValue("");
  };

  const getQuestions = async (e, value) => {
    e.preventDefault();
    appendItem(value);
    setValue("");

    try {
      const response = await fetch(
        "http://localhost:8000/send_question",
        {
          method: "POST", // Change the method to POST
          headers: {
            "Content-Type": "application/json",
            // Add any other headers as needed
          },
          body: JSON.stringify({ text: value }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Network response was not ok: ${response.status} - ${response.statusText}`
        );
      }

      let data;
      try {
        data = await response.json();
      } catch (jsonError) {
        console.error("Error parsing JSON:", jsonError.message);
        // Handle non-JSON responses here, if needed
        return;
      }

      console.log("Data:", data["question"]);
      appendItem(data["question"]);
      // Process the data as needed
    } catch (error) {
      console.error("Error fetching questions:", error.message);
    }
  };
  const messageSend = async (e) => {
    e.preventDefault();
    console.log(value);
    appendItem(value);
    setValue("");
    const response = await fetch(
      "http://localhost:8000/response",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: value }),
      }
    );

    const data = await response.json();
    console.log(data["response"]);
    const responseString = data["response"];
    // appendItem(responseString)
    const pattern = /content=/;
    const modifiedText = responseString.replace(pattern, "");
    appendItem(modifiedText.slice(1, -1));
    setValue("");
  };

  const openMapModal = () => {
    setMapModalOpen(true);
    clearChat();
    // appendItem("Choose location");
    dialog.current.showModal();
    console.log("open");
  };

  const closeMapModal = () => {
    setMapModalOpen(false);
    dialog.current.close();
  };

  const handelClick = async (e, value1, value2) => {
    console.log(value1, value2);
    const response = await fetch(
      "http://localhost:8000/get_data",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: `${value1},${value2}` }),
      }
    );
    const data = await response.json();
    console.log(data["data"]["data"]);
    // appendItem(data["data"]["image"]);
    setImage(data["data"]["image"]);
    dialog.current.close();
    getQuestions(e, "start chat");
  };
  //   const handleAnswer = (e, answer) => {
  //     e.preventDefault();
  //     appendItem(questions[currentQuestion]);
  //     appendItem(answer);
  //     const newAnswers = [...answers];
  //     newAnswers[currentQuestion] = answer;
  //     setAnswers(newAnswers);

  //     if (currentQuestion < 4) {
  //       setCurrentQuestion(currentQuestion + 1);
  //     } else {
  //       console.log('All questions answered:', newAnswers);
  //     }
  //   };

  return (
    <>
      <MapModal
        ref={dialog}
        handelClick={handelClick}
        onClose={closeMapModal}
        onFinish={getQuestions}
      />

      <div className="w-full h-screen">
        {image && <img src={image} alt="image" className="w-2/3 h-3/6" />}
        {chats.map((message, index) => (
          <Message message={message} index={index} image={image} />
        ))}
        {/* {chats.map((message, index)  => ( 
            <QuestionMessage index={index} message={chats[index]} questions={questions} appendItem={appendItem} setAnswers={setAnswers} currentQuestion={questions[index]} onAnswer={handleAnswer}/>
        ))} */}
      </div>

      {/* This is for chat */}
    {!props.flag && <div className="flex fixed bottom-0 p-6 bg-slate-700 w-full">
    <form onSubmit={(e) => getQuestions(e, value)} className="w-full flex">
        <input
        className="input w-full"
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        />
        <button type="submit" className="ml-4">
        <BsFillSendFill size={30} />
        </button>
        <button
        className="ml-4"
        onClick={(e) => {
            e.preventDefault();
            openMapModal();
        }}
        >
        <SiGooglemaps size={30} />
        </button>
    </form>
    </div>}
      {/* This is for questions */}
      {props.flag &&<div className="flex fixed bottom-0 p-6 bg-slate-700 w-full">
        <form onSubmit={messageSend} className="w-full flex">
          <input
            className="input w-full"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
          <button type="submit" className="ml-4">
            <BsFillSendFill size={30} />
          </button>
          <button className="ml-4" onClick={openMapModal}>
            <SiGooglemaps size={30} />
          </button>
        </form>
      </div>}
    </>
  );

}

export default Chatbox;

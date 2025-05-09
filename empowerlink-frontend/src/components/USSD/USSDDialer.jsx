import React, { useState } from "react";
import "./USSDDialer.css";
import { useLazyQuery } from "@apollo/client";
import { GET_USSD_MENU }    from "../../graphql/queries";

const USSDDialer = () => {
  // fullText holds the accumulated USSD input path (e.g., "1*2*3").
  const [fullText, setFullText] = useState("");
  // entry holds the current screen input (reset after each send).
  const [entry, setEntry] = useState("");
  const [response, setResponse] = useState("");

  const [fetchMenu] = useLazyQuery(GET_USSD_MENU, {
    variables: { phoneNumber: "0712345678", text: fullText },
    fetchPolicy: "no-cache",
    onCompleted: (data) => {
      let msg = data.getUSSDMenu.message || "";
      msg = msg.replace(/^(CON|END)\s*/, ""); // Strip CON/END at the start
      setResponse(msg);
      // Clear entry for next input
      setEntry("");
    },
    onError: () => {
      setResponse("⚠️ Error contacting USSD service.");
    },
  });

  const handleDial = () => {
    // Build the new fullText path
    const newFull = fullText ? `${fullText}*${entry}` : entry;
    setFullText(newFull);
      fetchMenu({
      variables: {
        phoneNumber: "0712345678",
        input: newFull
      }
    });
  };

  const handleKeyPress = (value) => {
    setEntry((prev) => `${prev}${value}`);
  };

  const handleClear = () => {
    setFullText("");
    setEntry("");
    setResponse("");
  };

  return (
    <div className="ussd-container">
      <div className="phone-screen">
        <div className="display">
          {/* Show last response or entry prompt */}
          <p>{response || "* Dial code here *"}</p>
          <p>{entry}</p>
        </div>
        <div className="keypad">
          {[1,2,3,4,5,6,7,8,9,"*",0,"#"].map((key) => (
            <button key={key} onClick={() => handleKeyPress(key)}>
              {key}
            </button>
          ))}
        </div>
        <div className="actions">
          <button className="dial-btn" onClick={handleDial}>Dial</button>
          <button className="clear-btn" onClick={handleClear}>Clear</button>
        </div>
      </div>
    </div>
  );
};

export default USSDDialer;

// const USSDDialer = () => {
//   const [input, setInput] = useState("");
//   const [response, setResponse] = useState("");
//
//   const [fetchMenu] = useLazyQuery(
//     GET_USSD_MENU,
//     {
//       variables: { phoneNumber: "0712345678", input },
//       fetchPolicy: "no-cache",
//       onCompleted: (data) => {
//         setResponse(data.getUSSDMenu.message);
//       },
//       onError: () => {
//         setResponse("⚠️ Error contacting USSD service.");
//       },
//     }
//   );
//
//   const handleDial = () => {
//     fetchMenu();
//   };
//
//
//   const handleKeyPress = (value) => {
//     setInput((prev) => prev + value);
//   };
//
//   const handleClear = () => {
//     setInput("");
//     setResponse("");
//   };
//
//   return (
//     <div className="ussd-container">
//       <div className="phone-screen">
//         <div className="display">
//           <p>{input || "*dial code here*"}</p>
//         </div>
//         <div className="keypad">
//           {[1,2,3,4,5,6,7,8,9,"*",0,"#"].map((key) => (
//             <button key={key} onClick={() => handleKeyPress(key)}>
//               {key}
//             </button>
//           ))}
//         </div>
//         <div className="actions">
//           <button className="dial-btn" onClick={handleDial}>Dial</button>
//           <button className="clear-btn" onClick={handleClear}>Clear</button>
//         </div>
//         <div className="response">
//           <p>{response}</p>
//         </div>
//       </div>
//     </div>
//   );
// };
//
// export default USSDDialer;
//

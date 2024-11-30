import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainProductSearch from "./mainPage/MainProductSearch.jsx";
import SecondProductSearch from "./secondPage/SecondProductSearch.jsx";
import { ToastContainer } from "react-toastify";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <ToastContainer />
      <Router>
        <Routes>
          <Route path="/" element={<MainProductSearch />} />
          <Route path="/resault" element={<SecondProductSearch />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;

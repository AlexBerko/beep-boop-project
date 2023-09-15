import React, { useEffect } from "react";

export default function MyRequests(props) {
  const token = localStorage.getItem("token");

  useEffect(() => {
    props.apiFunc("https://95.140.148.239/help/my/", "GET", token);
  }, [token]);

  console.log(props.recordsJS);
  console.log(props.recordsObj);

  return <div>MyRequests</div>;
}

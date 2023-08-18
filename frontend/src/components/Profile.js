import React, { useEffect } from "react";

export default function Profile(props) {
  useEffect(() => {
    props.apiFunc("http://127.0.0.1:8000/accounts/profile/", "GET");
  });

  console.log(props.recordsJS);
  return <div>Profile</div>;
}

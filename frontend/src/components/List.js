import React from "react";

export default function List(props) {
  return (
    <div>
      <p>Это страница со списком всех просьб</p>
      <button
        onClick={() => {
          props.onBtn();
          props.apiFunc("http://127.0.0.1:8000/help/24/", "GET");
          props.apiFunc(
            "https://api.checko.ru/v2/search?key=CAYR4QAsioUmKS5o&by=name&obj=org&query=ПАО Ростелеком&limit=1",
            "GET"
          );
        }}
      >
        Перейти к конкретному объявлению
      </button>
    </div>
  );
}

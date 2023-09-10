import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import List from "./List";
import "./List.css";

export default function Lists(props) {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  useEffect(() => {
    props.apiFunc("http://127.0.0.1:8000//help/list/", "GET", token);
  }, [token]);

  if (token === null) {
    navigate("/login", { replace: true });
  } else {
    return (
      <div className="mainpg">
        <div className="firstbaner">
          <div className="txt">
            <p className="maintxt">У вас есть больше, чем вам нужно?</p>
            <p className="secondtxt">Вы можете помочь нуждающимся!</p>
          </div>
          <div class="arrow-7">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <img
            className="baner"
            src={require("../img/baner.jpg")}
            alt={"Банер"}
          />
        </div>
        <div className="announc">
          {(() => {
            const options = [];

            for (let i = 0; i < props.recordsObj.length; i++) {
              options.push(
                <List
                  key={i}
                  arrayId={i}
                  apiFunc={props.apiFunc}
                  recordsObj={props.recordsObj}
                  recordsJS={props.recordsJS}
                  handler={props.handler}
                />
              );
            }

            return options;
          })()}
        </div>
      </div>
    );
  }
}

// class Lists extends Component {
//   constructor(props) {
//     super(props);

//     this.state = {
//       navigate: useNavigate()
//     };
//   }

//   componentDidMount() {
//     const token = localStorage.getItem("token");
//     this.props.apiFunc("http://127.0.0.1:8000//help/list/", "GET", token);
//   }

//   render() {
//     if (localStorage.getItem("token") === undefined) {
//       this.state.navigate("/login", { replace: true });
//       // history.push('/login')
//     } else {

//       return (
//         <div>
//           {(() => {
//             const options = [];

//             for (let i = 0; i < this.props.recordsObj.length; i++) {
//               options.push(
//                 <List
//                   key={i}
//                   arrayId={i}
//                   apiFunc={this.props.apiFunc}
//                   recordsObj={this.props.recordsObj}
//                   handler={this.props.handler}
//                 />
//               );
//             }

//             return options;
//           })()}
//         </div>
//       );
//         }
//   }
// }

// export default Lists;

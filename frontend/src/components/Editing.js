import React, { useState } from "react";
import { Button, Form, Input, DatePicker, Modal } from "antd";
import { useNavigate } from "react-router-dom";

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

const App = (props) => {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const token = localStorage.getItem("token");
  console.log(props.recordsJS);

  const onFinish = (values) => {
    const formData = new FormData();
    formData.append("title", values.title);
    formData.append("full_info", values.full_info);
    formData.append(
      "deadline_date",
      new Intl.DateTimeFormat("ru", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(values.deadline_date)
    );

    props.apiFunc(
      `https://95.140.148.239/help/${props.recordsJS.id}/`,
      "PUT",
      token,
      formData
    );
    setIsModalVisible(true);

    console.log(values);
  };

  const handleModalOk = () => {
    setIsModalVisible(false);
    navigate("/requests", { replace: true });
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px" }}>Введите данные заявки</h2>
      <form>
        <label>
          Text input1: <input type="text" value={props.recordsJS.title} />
        </label>
      </form>
      <label>
        Text input2: <input type="text" value={props.recordsJS.title} />
      </label>
      <Form
        {...layout}
        name="nest-messages"
        onFinish={onFinish}
        style={{
          maxWidth: 800,
        }}
      >
        <form>
          <label>
            Text input3: <input type="text" value={props.recordsJS.title} />
          </label>
        </form>
        <label>
          Text input4: <input type="text" value={props.recordsJS.title} />
        </label>
        <Form.Item
          name="title2"
          label="Название2"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <label>
            <input
              type="text"
              value={props.recordsJS.title}
              autocomplete="off"
            />
          </label>
        </Form.Item>
        <Form.Item
          name="title4"
          label="Название4"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <label>
            <Input
              type="text"
              value={props.recordsJS.title}
              autocomplete="off"
            />
          </label>
        </Form.Item>

        <Form.Item name="full_info" label="Описание">
          <Input.TextArea rows={9} value={props.recordsJS.full_info} />
        </Form.Item>

        <Form.Item name="deadline_date" label="Срок выполнения">
          <DatePicker />
        </Form.Item>

        <Form.Item
          wrapperCol={{
            ...layout.wrapperCol,
            offset: 8,
          }}
        >
          <Button type="primary" htmlType="submit">
            Сохранить
          </Button>
        </Form.Item>
      </Form>

      <Modal
        title="Изменения сохранены"
        visible={isModalVisible}
        onOk={handleModalOk}
        closable={false}
        maskClosable={false}
        onCancel={handleModalOk}
      />
    </div>
  );
};
export default App;

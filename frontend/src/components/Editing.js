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
  let [titleField, setTitleField] = useState(props.recordsJS.title);
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

  const handleChangeTitle = (e) => {
    setTitleField(e.target.value);
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px" }}>Введите данные заявки</h2>
      <form method="post">
        <label>
          Text input1:{" "}
          <input
            name="input1"
            type="text"
            value={titleField}
            onChange={handleChangeTitle}
          />
        </label>
      </form>
      <label>
        Text input2:{" "}
        <input
          name="input2"
          type="text"
          value={titleField}
          onChange={handleChangeTitle}
        />
      </label>
      <Form
        {...layout}
        name="nest-messages"
        onFinish={onFinish}
        style={{
          maxWidth: 800,
        }}
      >
        <form method="post">
          <label>
            Text input3:{" "}
            <input
              name="input3"
              type="text"
              value={titleField}
              onChange={handleChangeTitle}
            />
          </label>
        </form>
        <label>
          Text input4:{" "}
          <input
            name="input4"
            type="text"
            value={titleField}
            onChange={handleChangeTitle}
          />
        </label>
        <Form.Item
          name="title"
          label="Название"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <label>
            <Input
              type="text"
              value={titleField}
              onChange={handleChangeTitle}
            />
          </label>
        </Form.Item>
        <label>
          <Input
            name="title5"
            type="text"
            value={titleField}
            onChange={handleChangeTitle}
          />
        </label>

        <Form.Item name="full_info" label="Описание">
          <label>
            <Input.TextArea rows={9} value={props.recordsJS.full_info} />
          </label>
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

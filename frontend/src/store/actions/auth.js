import axios from "axios";
import * as actionTypes from "./actionTypes";

export const authStart = () => {
  return {
    type: actionTypes.AUTH_START,
  };
};

export const authRegDone = () => {
  return {
    type: actionTypes.AUTH_REGDONE,
  };
};

export const authLoading = () => {
  return {
    type: actionTypes.AUTH_LOADING,
  };
};

export const authSuccess = (token) => {
  return {
    type: actionTypes.AUTH_SUCCESS,
    token: token,
  };
};

export const authFail = (error) => {
  return {
    type: actionTypes.AUTH_FAIL,
    error: error,
  };
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("expirationDate");

  return {
    type: actionTypes.AUTH_LOGOUT,
  };
};

export const checkAuthTimeout = (expirationTime) => {
  return (dispatch) => {
    setTimeout(() => {
      dispatch(logout());
    }, expirationTime * 1000);
  };
};

export const authLogin = (email, password) => {
  return (dispatch) => {
    dispatch(authStart());
    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    axios
      .post("https://95.140.148.239/user/login/", formData)
      .then((res) => {
        localStorage.setItem("hash", res.data.hash);
        document.location.href = `https://95.140.148.239/otp/${res.data.hash}/`;
      })
      .catch((err) => {
        console.log(err);
        dispatch(authFail(err));
      });
  };
};

export const authOtp = (otp) => {
  return (dispatch) => {
    dispatch(authStart());
    const formData = new FormData();
    formData.append("otp", otp);
    formData.append("hash", localStorage.getItem("hash"));

    axios
      .post(
        "https://95.140.148.239/user/otp/",
        formData,
        localStorage.getItem("hash")
      )
      .then((res) => {
        console.log(res);
        const token = res.data.auth_token;
        localStorage.setItem("token", token);
        const expirationDate = new Date(new Date().getTime() + 3600 * 1000);
        localStorage.setItem("expirationDate", expirationDate);
        dispatch(authSuccess(token));
        dispatch(checkAuthTimeout(3600));
        document.location.href = `https://95.140.148.239/`;
      })
      .catch((err) => {
        console.log(err);
        dispatch(authFail(err));
      });
  };
};

export const authSignup = (
  username,
  email,
  phone_no,
  head,
  ogrn,
  inn,
  address_reg,
  address_fact,
  is_rest,
  is_ind_pred,
  password1,
  password2
) => {
  return (dispatch) => {
    dispatch(authStart());
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("phone_no", phone_no);
    formData.append("head", head);
    formData.append("ogrn", ogrn);
    formData.append("inn", inn);
    formData.append("address_reg", address_reg);
    formData.append("address_fact", address_fact);
    formData.append("is_rest", is_rest);
    formData.append("is_ind_pred", is_ind_pred);
    formData.append("password1", password1);
    formData.append("password2", password2);

    axios
      .post("https://95.140.148.239/user/register/", formData)
      .then((res) => {
        dispatch(authLoading());
        dispatch(authRegDone());
        document.location.href = `https://95.140.148.239/login/`;
      })
      .catch((err) => {
        dispatch(authFail(err));
      });
  };
};

export const authCheckState = () => {
  return (dispatch) => {
    const token = localStorage.getItem("token");
    if (token === undefined) {
      dispatch(logout());
    } else {
      const expirationDate = new Date(localStorage.getItem("expirationDate"));
      if (expirationDate <= new Date()) {
        dispatch(logout());
      } else {
        dispatch(authSuccess(token));
        dispatch(
          checkAuthTimeout(
            (expirationDate.getTime() - new Date().getTime()) / 1000
          )
        );
      }
    }
  };
};

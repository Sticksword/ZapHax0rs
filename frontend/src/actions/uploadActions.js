import Axios from 'axios';

const uploadFileSuccess = (uploads) => {
  return {
    type: 'UPLOAD_SUCCESS',
    uploads
  };
};

const uploadDemoSuccess = (demo) => {
  return {
    type: 'DEMO_SUCCESS',
    demo
  };
};

export const uploadFile = (file) => {
  return (dispatch) => {
    // console.log(file);
    return Axios.post('http://localhost:5000/upload', file)
      .then(response => {
        dispatch(uploadFileSuccess(response.data));
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const uploadDemo = (demo) => {
  return (dispatch) => {
    return Axios.post('http://localhost:5000/demo', demo)
      .then(response => {
        dispatch(uploadDemoSuccess(response.data));
      })
      .catch(error => {
        throw(error);
      });
  };
};

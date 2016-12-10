const INITIAL_STATE = { files: [] };

const FilesReducer = function(state = [], action) {
  switch (action.type) {
    case 'UPLOAD_SUCCESS':
      return [
        ...state,
        Object.assign({}, action.uploads)
      ];

    case 'DEMO_SUCCESS':
      return [
        ...state,
        Object.assign({}, action.demo)
      ];

    default:
      return state;
  }
};

export default FilesReducer;

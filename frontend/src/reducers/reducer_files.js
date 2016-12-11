let id = 0; // l0l hax

const FilesReducer = function(state = [], action) {
  switch (action.type) {
    case 'UPLOAD_SUCCESS':
      console.log('upload success');
      let uploadsWithIds = [];
      action.uploads.forEach((obj) => {
        obj.id = id;
        id++;
        uploadsWithIds.push(obj);
      });
      return [
        ...state,
        ...uploadsWithIds
      ];

    case 'DEMO_SUCCESS':
      console.log('demo success');
      let test2 = Object.assign({}, action.demo);
      test2.id = id;
      id++;
      return [
        ...state,
        test2
      ];

    default:
      return state;
  }
};

export default FilesReducer;

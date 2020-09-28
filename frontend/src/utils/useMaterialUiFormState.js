import React, { useState } from "react";
import MuiAlert from "@material-ui/lab/Alert";

const FormErrors = ({ show }) => {
  if (show) {
    return (
      <MuiAlert variant="outlined" severity="error">
        Please correct the errors in the form
      </MuiAlert>
    );
  }
  return <React.Fragment />;
};

// export const dataFromState = ({ state }) => {
//   let data = {};

//   Object.keys(state).forEach((key) => {
//     data[key] = state[key].value || state[key].checked || false;
//   });
//   return data;
// };

export default function useMaterialUiFormState(fieldDescriptions) {
  let initialState = {};

  Object.keys(fieldDescriptions).forEach((key) => {
    const fieldType = fieldDescriptions[key].fieldType || "TextField";

    switch (fieldType) {
      case "TextField":
        initialState[key] = {
          value: fieldDescriptions[key].default || "",
          error: false,
          errorMessage: "",
        };
        break;
      case "Checkbox":
        initialState[key] = {
          checked: fieldDescriptions[key].default || false,
        };
        break;

      default:
        throw new Error(`Unknown Field Type ${fieldType}`);
    }
  });
  const [state, updateState] = useState(initialState);

  const dataFromState = () => {
    let data = {};
    Object.keys(state).forEach((key) => {
      const fieldType = fieldDescriptions[key].fieldType || "TextField";
      switch (fieldType) {
        case "TextField":
          data[key] = state[key].value || "";
          break;
        case "Checkbox":
          data[key] = state[key].checked || false;

          break;
        default:
          throw new Error(`Unknown Field Type ${fieldType}`);
      }
    });
    return data;
  };

  const handleChange = (key) => {
    return (event) => {
      updateState({
        ...state,
        [key]: {
          ...state[key],
          value: event.target.value,
          checked: event.target.checked,
        },
      });
    };
  };

  //   const handleChangeCheckbox = (key) => {
  //     return (event) => {
  //       updateState({
  //         ...state,
  //         [key]: {
  //           ...state[key],
  //           checked: event.target.checked,
  //         },
  //       });
  //     };
  //   };

  let fieldProps = {};
  Object.keys(fieldDescriptions).forEach((key) => {
    const fieldType = fieldDescriptions[key].fieldType || "TextField";

    const commonProps = {
      onChange: handleChange(key),
    };

    switch (fieldType) {
      case "TextField":
        fieldProps[key] = {
          ...commonProps,
          value: state[key].value,
          error: state[key].error ? state[key].error : null,
          helpertext: state[key].errorMessage,
          required: fieldDescriptions[key].required || false,
        };

        break;
      case "Checkbox":
        fieldProps[key] = {
          ...commonProps,
          checked: state[key].checked,
        };
        break;
      default:
        throw new Error(`Unknown Field Type ${fieldType}`);
    }
  });

  const formErrors = <FormErrors />;

  return [state, fieldProps, formErrors, dataFromState];
}

function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function validateName(name) {
  const re = /^([a-zA-Z',.-]+( [a-zA-Z',.-]+)*){2,30}$/;
  return re.test(String(name).toLowerCase());
}

export const validators = {
  email: ({ state, value }) => {
    if (validateEmail(value)) return;
    return `Please enter a valid email address`;
  },

  firstOrLastName: ({ state, value }) => {
    if (validateName(value)) return;
    return `Please enter a valid name`;
  },
  goodPassword: ({ state, value }) => {},
  mustBeChecked: ({ state, value }) => {
    if (!value) return `Checkbox must be checked`;
  },
  exactMatch: ({ valueToMatch, errorMessage }) => {
    return ({ state, value }) => {
      if (state[valueToMatch] !== value) return errorMessage;
    };
  },
};

// TODO: actually use the validators and show error messages
// on form submit
// on loose focus
// on change, cancel errors once valid only

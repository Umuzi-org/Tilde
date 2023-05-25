import { Action } from "../index.mjs";
import { STATUS_ERROR } from "../../consts.mjs";

export default class NotImplemented extends Action {
  name = "not implemented";

  action = async function () {
    return {
      status: STATUS_ERROR,
      message: "The current marker is not fully implemented!",
    };
  };
}

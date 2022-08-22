import { connect } from "react-redux";
import { useTraceUpdate } from "../../../hooks.js";
import { routes } from "../../../routes.js";

const RedirectorUnconnected = ({ authUser }) => {

  useTraceUpdate({authUser});

  window.location = routes.userBoard.route.path.replace(
    ":userId",
    authUser.userId
  );
};

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
    // whoAmICallStatus: state.WHO_AM_I,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

const Redirector = connect(
  mapStateToProps,
  mapDispatchToProps
)(RedirectorUnconnected);

export default Redirector;

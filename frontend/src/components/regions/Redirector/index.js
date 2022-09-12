import { connect } from "react-redux";
import { routes } from "../../../routes.js";

function RedirectorUnconnected({ authUser }) {
  window.location = routes.userBoard.route.path.replace(
    ":userId",
    authUser.userId
  );
}

const mapStateToProps = (state) => {
  return {
    authUser: state.App.authUser,
  };
};

const mapDispatchToProps = () => {
  return {};
};

const Redirector = connect(
  mapStateToProps,
  mapDispatchToProps
)(RedirectorUnconnected);

export default Redirector;

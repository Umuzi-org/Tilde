import React from "react";
import Presentation from "./Presentation";
// import { apiReduxApps } from "../../../../apiAccess/redux/apiApps";
import { connect } from "react-redux";

function UserDetailedStatsUnconnected({ userId }) {

    render(){
        const props = {}
        return <Presentation {...props}/>
    }
}

const mapStateToProps = (state) => {
  return {};
};

const mapDispatchToProps = (dispatch) => {
  return {};
};

const UserDetailedStats = connect(
  mapStateToProps,
  mapDispatchToProps
)(UserDetailedStatsUnconnected);
export default UserDetailedStats;

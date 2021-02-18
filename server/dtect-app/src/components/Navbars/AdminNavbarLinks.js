import React from "react";

import { NavLink } from "react-router-dom";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import Notifications from "@material-ui/icons/Notifications";
import Search from "@material-ui/icons/Search";
// core components
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";

import styles from "assets/jss/material-dashboard-react/components/headerLinksStyle.js";

const useStyles = makeStyles(styles);

var notifRedDotDisplay = "block";

export default function AdminNavbarLinks() {
  const classes = useStyles();
  return (
    <div>
      {/* {searchBar(classes)} */}
      {notifications(classes)}
    </div>
  );
}

export function searchBar(classes) {

  return (
    <div className={classes.searchWrapper}>
      <CustomInput
          formControlProps={{className: classes.margin + " " + classes.search}}
           inputProps={{placeholder: "Search", inputProps: {"aria-label": "Search"}}}
         />
      <Button color="white" aria-label="edit" justIcon round>
        <Search />
      </Button>
    </div>
  );
}

export function notifications(classes){
  return (<div className={classes.manager}>
        <NavLink
              to={"/admin/notifications"}
              className={classes.itemLink}
              activeClassName="active"
              style={{color: 'grey'}}
              onClick={() => onoff()}
            >
          <Button
            color={window.innerWidth > 959 ? "transparent" : "white"}
            justIcon={window.innerWidth > 959}
            simple={!(window.innerWidth > 959)}
            className={classes.buttonLink}
          >
            <Notifications className={classes.icon}/>
            <span className={classes.notifications} style={{display: notifRedDotDisplay}}></span>
          </Button>
        </NavLink>
      </div>
  );
}

export function onoff() {
    return (notifRedDotDisplay = 'none')
}

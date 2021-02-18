/*eslint-disable*/
import React, { useState, useEffect } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import AddAlert from "@material-ui/icons/AddAlert";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Button from "components/CustomButtons/Button.js";
import SnackbarContent from "components/Snackbar/SnackbarContent.js";
import Snackbar from "components/Snackbar/Snackbar.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";
import { fetchauthlogs } from "helpers/api_fetches.js";
import Table from "components/Table/Table.js";

const styles = {
  cardCategoryWhite: {
    "&,& a,& a:hover,& a:focus": {
      color: "rgba(255,255,255,.62)",
      margin: "0",
      fontSize: "14px",
      marginTop: "0",
      marginBottom: "0"
    },
    "& a,& a:hover,& a:focus": {
      color: "#FFFFFF"
    }
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none",
    "& small": {
      color: "#777",
      fontSize: "65%",
      fontWeight: "400",
      lineHeight: "1"
    }
  }
};

const useStyles = makeStyles(styles);

export default function Notifications() {
  const classes = useStyles();

  const [ tableRows, setTableRows ] = useState([[null]]);
  const [ tableFlags, setTableFlags ] = useState([[null]]);
  var rows = [];
  var flags = [];

  useEffect(() => {
    fetchauthlogs().then(logs => {
      var i;
      for (i = 0; i < logs.length; i++) {
        var log = logs[i];
        var row = [log.time, log.source_user, log.destination_user, log.source_computer, log.destination_computer, log.authentication_type, log.logon_type, log.auth_orientation, log.auth_result];
        if (log.flagged) {
          rows.push(row);
          flags.push(log.flagged);
        }
      }
      // sort by time (most recent first)
      rows.sort(function(a,b){return b[0] - a[0];});
      setTableRows(rows);
      setTableFlags(flags);
    });
  }, [5000]);


  return (
    <GridContainer>
      <GridItem xs={12} sm={12} md={12}>
        {getTable(tableRows, tableFlags)}
      </GridItem>
    </GridContainer>
  );
}

export function getNotif(notifMsg, notifColor){
    return (
      <SnackbarContent
        message={
          notifMsg
        }
        close
        color={notifColor}
        >
        </SnackbarContent>
    );
}

export function getTable(rows, flags) {
  return (
    <Table
      tableHeaderColor="primary"
      tableHead={["Time", "Source User", "Destination User", "Source Computer", "Destination Computer", "Authentication Type", "Logon Type", "Auth Orientation", "Auth Result"]}
      tableData={rows}
      tableDisplay={flags}
    ></Table>
  );
}
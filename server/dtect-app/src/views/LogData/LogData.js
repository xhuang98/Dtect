import React, { useState, useEffect } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

import Info from "@material-ui/icons/Info";
import { fetchauthlogs } from "helpers/api_fetches.js";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";
import { setEmitFlags } from "typescript";

const styles = {
  cardCategoryWhite: {
    "&,& a,& a:hover,& a:focus": {
      marginTop: "0",
      marginBottom: "0",
      color: "rgba(255,255,255,.62)",
      fontSize: "14px",
      margin: "0"
    },
    "& a,& a:hover,& a:focus": {
      color: "#FFFFFF"
    },
    "& svg": {
      top: "4px",
      width: "20px",
      height: "20px",
      position: "relative",
      marginRight: "3px",
      marginLeft: "3px"
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

export default function LogData() {
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
        rows.push(row);
        flags.push(log.flagged);
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
        <Card>
          <CardHeader color="primary">
            <h4 className={classes.cardTitleWhite}>Activities</h4>
            <p className={classes.cardCategoryWhite}>
            <Info/>Suspicious Activities Are Coloured in Red
            </p>
          </CardHeader>
          <CardBody>
            {getTable(tableRows, tableFlags)}
          </CardBody>
        </Card>
      </GridItem>
    </GridContainer>
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

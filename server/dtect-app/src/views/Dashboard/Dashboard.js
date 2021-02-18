import React, { useState, useEffect } from "react";
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import AssignmentTurnedIn from '@material-ui/icons/AssignmentTurnedIn';
import Info from '@material-ui/icons/InfoOutlined';
import Ballot from "@material-ui/icons/Ballot";
import Warning from "@material-ui/icons/Warning";
import DateRange from "@material-ui/icons/DateRange";
import Computer from "@material-ui/icons/Computer";
import CheckCircle from '@material-ui/icons/CheckCircle';
import Update from "@material-ui/icons/Update";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import AccessTime from "@material-ui/icons/AccessTime";
import Accessibility from "@material-ui/icons/Accessibility";
import Help from '@material-ui/icons/Help';
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";

import { fetchauthlogs } from "helpers/api_fetches.js";

import {
  dailySalesChart,
  emailsSubscriptionChart,
  completedTasksChart
} from "variables/charts.js";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import { set } from "mobx";

const useStyles = makeStyles(styles);

export default function Dashboard() {
  const classes = useStyles();
  var table = getTable();


  const [ data, setData ] = useState([{time:0}]);
  const [ anomolyCount, setAnomolyCount ] = useState(0);
  const [ userCount, setUserCount ] = useState(0);
  const [ successRate, setSuccessRate ] = useState(0);
  const [ activityCount, setActivityCount ] = useState(0);
  const [ userThreatRows, setUserThreatRows ] = useState([[]]);
  const [ typeThreatRows, setTypeThreatRows ] = useState([[]]);
  useEffect(() => {
    fetchauthlogs().then(logs => {
      setData(logs);

      // get anomoly count
      let count = 0;
      let userSet = new Set();
      let successCount = 0;
      let i = 0;
      for (i = 0 ; i < logs.length ; i++) {
        if (logs[i].flagged) {
          count += 1;
        }
        userSet.add(logs[i].source_user);
        if (logs[i].auth_result === "Success") {
          successCount += 1;
        }
      }
      setAnomolyCount(count);
      setUserCount(userSet.size);
      setSuccessRate((successCount / logs.length) * 100);
      setActivityCount(logs.length);

      setUserThreatRows(getThreatPercentageRows(logs, "source_user"));
      setTypeThreatRows(getThreatPercentageRows(logs, "authentication_type"));

    });
  }, [5000]);

  return (
    <div>
      <GridContainer>
        {smallCards(classes, 'warning', AssignmentTurnedIn, "Success Rate", successRate+"%", CheckCircle, "Get more space")}
        {smallCards(classes, 'success', Ballot, "Activity Count", activityCount, DateRange, "Total Number of Activities")}
        {smallCards(classes, 'danger', Warning, "Anomalies Count", anomolyCount, Help, "Total Number of Predicted Outliers")}
        {smallCards(classes, 'info', Accessibility, "Users", userCount, Computer, "Total Number of User Entities")}
      </GridContainer>
      <GridContainer>
        {largeCards(classes, "warning","User Threat Level","Flagged Events Percentage per User",getTable("User", userThreatRows))}
        {largeCards(classes, "primary","Authentication Type Threat Level","Flagged Events Percentage per Authentication Type",getTable("Authentication Type", typeThreatRows))}
      </GridContainer>
    </div>
  );
}

export function smallCards(classes, iconColor, Icon, category, title, FooterIcon, footer){
  return (
    <GridItem xs={12} sm={6} md={3}>
      <Card>
        <CardHeader color={iconColor} stats icon>
          <CardIcon color={iconColor}>
            <Icon/>
          </CardIcon>
          <p className={classes.cardCategory}>{category}</p>
          <h3 className={classes.cardTitle}>
            {title}
          </h3>
        </CardHeader>
       <CardFooter stats>
          <div className={classes.stats}>
            <FooterIcon />
            {footer}
          </div>
        </CardFooter>
      </Card>
  </GridItem>);
}

export function graphs(classes, headerColor, graph, type, title, category, isComparison) {
  return (
    <GridItem xs={12} sm={12} md={4}>
          <Card chart>
            <CardHeader color={headerColor}>
              <ChartistGraph
                className="ct-chart"
                data={graph.data}
                type={type}
                options={graph.options}
                listener={graph.animation}
              />
            </CardHeader>
            <CardBody>
              <h4 className={classes.cardTitle}>{title}</h4>
              <p className={classes.cardCategory}>
                {renderComparison(classes, isComparison)}
                {category}
              </p>
            </CardBody>
          </Card>
        </GridItem>
  );
}

export function renderComparison(classes, isComparison){
    if (isComparison) {
      return (
          <p>
          <span className={classes.successText}>
              <ArrowUpward className={classes.upArrowCardCategory} /> 55%
          </span>
            {" "}
            increase in todays activities
          </p>
      );
    }
}

export function largeCards(classes, headerColor, title, category, body) {
  return (
    <GridItem xs={12} sm={12} md={6}>
          <Card>
            <CardHeader color={headerColor}>
              <h4 className={classes.cardTitleWhite}>{title}</h4>
              <p className={classes.cardCategoryWhite}>
                {category}
              </p>
            </CardHeader>
            <CardBody>
              {body}
            </CardBody>
          </Card>
        </GridItem>
  );
}

export function getTable(columnName, rows){
  return (
    <Table
      tableHeaderColor="warning"
      tableHead={[columnName, "Number of Anomalies", "Total Events", "Percentage of Flagged Events"]}
      tableData={rows}
    />
  );
}

// construct row for threat level table table [columnName, # anomalies, # activties, threat %]
// input: auth logs from fetch, column name in the auth log that you want to aggregate
// output null if columnName is not in the auth logs table
export function getThreatPercentageRows(data, columnName) {
  if (!data[0].hasOwnProperty(columnName)) {
    return null;
  }

  // get types
  let threatLevels = {};
  let i = 0;
  for (i = 0 ; i < data.length; i++) {
    let colval = data[i][columnName];
    if (colval == null) {
      colval = "Unknown";
    }
    let isFlagged = data[i].flagged;
    if (threatLevels.hasOwnProperty(colval)) {
      threatLevels[colval].total += 1;
    } else {
      threatLevels[colval] = {};
      threatLevels[colval].total = 1;
      threatLevels[colval].anomaly = 0;
    }

    if (isFlagged) {
      threatLevels[colval].anomaly += 1;
    }

    // update percentage
    if (threatLevels[colval].total > 0) {
      threatLevels[colval].percentage = ((threatLevels[colval].anomaly / threatLevels[colval].total) * 100).toFixed(2) + "%";
    }
  }

  let threatRows = [];
  for (const [key, value] of Object.entries(threatLevels)) {
    threatRows.push([key, value.anomaly, value.total, value.percentage]);
  }
  // sort in descending order of percentage
  threatRows.sort(function(a,b){return b[1]/b[2] - a[1]/a[2];});

  return threatRows;
}
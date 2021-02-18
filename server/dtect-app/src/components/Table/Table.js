import React from "react";
import PropTypes from "prop-types";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
// core components
import styles from "assets/jss/material-dashboard-react/components/tableStyle.js";

const useStyles = makeStyles(styles);

export default function CustomTable(props) {
  const classes = useStyles();
  const { tableHead, tableData, tableHeaderColor, tableDisplay} = props;
  return (
    <div className={classes.tableResponsive}>
      <Table className={classes.table}>
        {tableHead !== undefined ? (getTableHead(classes, tableHead, tableHeaderColor)) : null}
        {getTabelBody(classes, tableData, tableDisplay)}
      </Table>
    </div>
  );
}

export function getTableHead(classes, tableHead, tableHeaderColor){
  return (
          <TableHead className={classes[tableHeaderColor + "TableHeader"]}>
            <TableRow className={classes.tableHeadRow}>
              {tableHead.map((prop, key) => {
                return (
                  <TableCell
                    className={classes.tableCell + " " + classes.tableHeadCell}
                    key={key}
                  >
                    {prop}
                  </TableCell>
                );
              })}
            </TableRow>
          </TableHead>
        
  );
}

export function getTabelBody(classes, tableData, tableDisplay){
  return (
        <TableBody>
          {tableData.map((prop, key) => {
            if (tableDisplay != null && tableDisplay[key] == true){
              return (
                tableCellDisplay(prop, key, classes, classes.tableCellRed)
              );
            } else {
              return (
                tableCellDisplay(prop, key, classes, classes.tableCell)
              );
            }

            
          })}
        </TableBody>
  );
}

export function tableCellDisplay(prop, key, classes, displayClass){
    return (
    <TableRow key={key} className={classes.tableBodyRow}>
      {prop.map((prop, key) => {
        return (
          <TableCell className={displayClass} key={key}>
            {prop}
          </TableCell>
        );
      })}
    </TableRow>);
}

CustomTable.defaultProps = {
  tableHeaderColor: "gray"
};

CustomTable.propTypes = {
  tableHeaderColor: PropTypes.oneOf([
    "warning",
    "primary",
    "danger",
    "success",
    "info",
    "rose",
    "gray"
  ]),
  tableHead: PropTypes.arrayOf(PropTypes.string),
  tableData: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string))
};

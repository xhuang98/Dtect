# Demo Write-Up

Demo Video: https://drive.google.com/file/d/1J94VWlzdt97txBHj1s8HzNXee9aUvXv3/view?usp=sharing

## Frontend
- Login page

- Main Dashboard that displays aggregates
  - Statistical aggregations
  - Tables

- Log Data page displays all log activities
  - Table containing all logs
  - Anomalous activities are distinguished from non-anomalous activities

- Anomalies page
  - Displays all predictions/anomalous activities by the data analysis model

- Notification button
  - Route to the anomalies page with an indicator for newly raised alerts 
  
- Future plans:
  - Log popup
        - Logs are clickable with a popup window that displays other details including a button to the user's profile       
  - User profile
        - From the log popup, the user profile button goes to user's details and their log activity history     
  - Timeline
        - A timeline that shows the number of activities with histogram in real-time
  - Charts and graphs 
        - Dynamic charts and graphs aggregations for the dashboard
## Backend
### Server
- Handles routing and data storage
- Provides dynamic data to the front end
### Data analytics
- Auto-encoder structure for outlier detection
- Considers a single user's most recent activities, determine whether the activity window is an outlier from past activities of peers
- Future plans:
  - Improve performance
  - Control false positive rate

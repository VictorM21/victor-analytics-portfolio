&nbsp;Real-time Data Pipeline Project



&nbsp;Overview

A complete real-time data pipeline that generates, processes, and visualizes clickstream data.



&nbsp;Components

\- Producer: Generates 10 clicks/second and saves to JSON

\- Consumer: Reads and processes click data in real-time

\- Dashboard: Flask + Socket.IO web interface with live charts



&nbsp;How to Run



1\. Start all components:



python scripts/run\_all.py



Choose option 1



2\. Open dashboard:

\- Go to http://localhost:5000



3\. Individual components:

\- Producer only: `python producer/click\_producer.py`

\- Consumer only: `python consumer/click\_consumer.py`

\- Dashboard only: `python dashboard/app.py`



&nbsp;Features

\- Live click generation (10/sec)

\- Real-time data processing

\- Interactive charts updating every 2 seconds

\- Connection status indicator

\- Multiple data views (pages, devices, countries, activity)



&nbsp;Technologies

\- Python

\- Flask

\- Socket.IO

\- Chart.js

\- Threading


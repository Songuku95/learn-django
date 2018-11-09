# Python Entry Task

The Python Entry Task aims to help you acquaint yourself with the fundamentals of web server programming and the various concepts in this area (or if you're already experienced, to help you revise them). It tests your relevant technical skills and learning abilities, as well as serves as a guide for future job assignments.

# Project Description

You are to design and build up the server infrastructure for a social event sharing platform. In the platform, visitors can view events in various conditions, like and participant their favorite events, and view other people’s activities.

1. Visitors need to login to view events.
2. Visitors can browse a **paginated** list of events, and search for specific events by date ranges and channels [i.e. event tags/categories whatever you name it].
3. Visitors can view event details, including title, descriptions, event photos, event date and location, list of participants, list of likes, and comments. He or she can comment, like or participate in an event as well.

In addition, an admin interface should be built for administrators to create events containing the data mentioned in point (3).

## The Task (7 calendar days)

### a. API Endpoint and Database Design (to be completed latest by the 2nd day)

Design a suitable database schema and a set of API endpoints based on the description of the application in (2). Please consult mentors to clarify on feature requirements.

+ Each API documented should clearly state the request and response structure, and all possible response / error cases.
+ The database schema should be prepared in the form of SQL `CREATE TABLE` statements.
+ Please follow the guideline in [Python Development Guide](python-development-guide). If you're not sure why we have these practices, you can think about it ;) then look for your mentor for clarification.

### b. API Server Implementation

Implement a backend server to host relevant API endpoints and connect to the database. Depending on the situation, a pre-existing set of API endpoint and database design may be given, or the design from a. may be used.

**The API endpoints should not render any web pages (HTML documents); rather, it should only return the necessary data (in a format of your choice) to be processed by the front-end static assets (Javascript).**

### c. Admin Website Implementation

Implement an administrative website to provide power users to login and create events, as described in (2).

+ The admin user must be able to **upload images** to be displayed in the front end.
+ There is no design requirement on the admin website.

### d. Server Deployment

The API and admin servers should then be deployed as a WSGI application.

### e. Web Server Setup

Setup a web server (in nginx) that handles communication between the http request and the application servers.

##### The WSGI application and nginx configuration should be tweaked in order to support the performance requirements below.

## Design Constraints

#### Infrastructure

+ The server should be run in a virtual machine running **CentOS 7** *without GUI*.
  + Use **SSH** to access the server when deploying the project.
+ MySQL should be used as the database server.
+ nginx should be used as the web server.

#### Application

+ The API / backend server implementation should be based on **Django 1.11.x**.
+ Both API / backend servers should be in a single Django project.
+ **The following performance requirements are to be met**:
  + The API server should support up to 500 concurrent logins (**with each request using a different credential**) per second.
     + Each table in your designed database should contain at least 1 million entries of dummy data.
  + VM specs: Dual-core, 1GB RAM
+ The following Django-provided apps may not be used:
  + django.contrib.admin
  + django.contrib.auth
  + django.contrib.sessions
+ Third-party Django modules that performs large abstractions (e.g. Django REST Framework) are generally not allowed. Please consult with your mentors before using them.
+ For the admin website, Django's built-in admin site is not allowed. You have to write your own admin website templates and logic.
+ Testing is optional but recommended.

## Design Considerations

+ Robustness
+ Security
+ Performance

## Deliverables

+ Project source
+ Project distribution - Instructions on how to set up the application on a fresh server. This includes:
  + Dependencies installation
  + nginx configuration
  + Starting the server
  + (It would be good if a one-click shell script can be set up to perform the aforementioned tasks)
+ Documents
  + Design document
  + Installation and maintenance document
  + Performance test report
  + Concluding report

## Useful links
+ [Nginx](http://nginx.org/)
+ [MySQL](https://www.mysql.com/)


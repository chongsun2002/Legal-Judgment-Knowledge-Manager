# Legal Judgment Knowledge Manager

# User Guide

## Installation Instructions
1. Install Python 3.12.7 [here](https://www.python.org/downloads/release/python-3127/)
2. Clone the repository onto your local machine

# Developer Guide

## Directory Structure

### Controllers
The controllers folder contains the route handlers for all requests made to the Flask application.

### Services
The buiness logic layer called by the methods in `/controllers` after data is received. The directory structure of `/services` corresponds to `/controllers`.

### Models
Pydantic models for strong typing, data validation and integrity. Follows the directory structure of services and controllers.

### Features
The features that the business layer logic relies on.  
For example, extract.py contains text-preprocessing features which `judgments_service.py`'s upload function will rely on.

# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /home/pi/git/Hexapod

# Define environment variable
ENV Hexapod

# Run app.py when the container launches
CMD [ "python", "./VehicleMain.py" ]

# Use an official Node runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app
# Install dependencies
# Copy both package.json AND package-lock.json directly from the current directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Bundle app source
COPY . .

# Expose port for the application
EXPOSE 5173  

# Command to run your app
CMD ["npm", "run", "dev"]

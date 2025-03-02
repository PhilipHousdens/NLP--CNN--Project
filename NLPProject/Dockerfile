# Use the official Node.js image from the Docker Hub
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the frontend code to the container
COPY . /app/

# Build the Vue app
RUN npm run build

# Use nginx to serve the built frontend
FROM nginx:alpine

# Copy the built files from the previous stage
COPY --from=0 /app/dist /usr/share/nginx/html

# Expose the frontend port
EXPOSE 80

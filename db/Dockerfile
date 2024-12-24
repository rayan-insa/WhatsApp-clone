# Use the official MySQL image as the base image
FROM mysql:8.0

# Set environment variables for MySQL root user and default database
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=messagely

# Copy the initialization SQL script into the container
# MySQL will automatically execute any `.sql` files in this directory when the container starts
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306

# The default command is already set in the MySQL base image to run mysqld

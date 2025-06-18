FROM postgres:15

# Set environment variables
ENV POSTGRES_USER=spotify_user
ENV POSTGRES_PASSWORD=spotify_password
ENV POSTGRES_DB=spotify_oltp

# Copy initialization scripts
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Set permissions
RUN chmod -R 755 /docker-entrypoint-initdb.d/ 
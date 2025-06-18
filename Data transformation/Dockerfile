# Use jupyter/pyspark-notebook as base image
FROM jupyter/pyspark-notebook:latest

# Switch to root to make changes
USER root

# Create and set permissions for app directory
RUN mkdir -p /app && chown -R jovyan:users /app

# Ensure spark logs directory exists and has proper permissions
RUN mkdir -p /opt/spark/logs && chown -R jovyan:users /opt/spark/logs

# Switch back to notebook user
USER jovyan

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=jovyan:users . /app

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
if [ "$SPARK_MODE" = "master" ]; then\n\
    echo "Starting Spark Master..."\n\
    $SPARK_HOME/sbin/start-master.sh\n\
    sleep 10\n\
    echo "Starting Jupyter Notebook..."\n\
    cd /app && jupyter notebook --config=/app/.jupyter/jupyter_notebook_config.py &\n\
    echo "Waiting for services..."\n\
    tail -f /opt/spark/logs/spark-*-master-*.out\n\
elif [ "$SPARK_MODE" = "worker" ]; then\n\
    echo "Starting Spark Worker..."\n\
    $SPARK_HOME/sbin/start-worker.sh $SPARK_MASTER_URL\n\
    tail -f /opt/spark/logs/spark-*-worker-*.out\n\
fi' > /app/start.sh && chmod +x /app/start.sh

# Use the startup script
CMD ["/app/start.sh"]
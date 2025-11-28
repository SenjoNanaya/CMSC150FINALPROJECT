FROM rocker/r-ver:4.2.2

RUN apt-get update -qq && apt-get install -y \
  libssl-dev \
  libcurl4-gnutls-dev

# Install R packages
RUN R -e "install.packages(c('plumber', 'jsonlite'))"

# Copy your files
COPY plumber_project.R /app/plumber_project.R

# Open port 8000
EXPOSE 8000

# Run Plumber
CMD ["R", "-e", "pr <- plumber::plumb('/app/plumber_project.R'); pr$run(host='0.0.0.0', port=8000)"]
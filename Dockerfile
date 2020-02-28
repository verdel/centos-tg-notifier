FROM verdel/centos-base:latest
LABEL maintainer="Vadim Aleksandrov <valeksandrov@me.com>"

# Install Flask
RUN pip3 install --upgrade pip \
    && pip3 install coverage rednose nose \
    && pip3 install Flask Flask-Admin Flask-HTTPAuth Flask-Login flask-mongoengine Flask-RESTful python-telegram-bot gunicorn emoji PySocks \
    # Clean up
    && dnf clean all \
    && rm -rf \
    /usr/share/man \
    /tmp/* \
    /var/cache/dnf

# Expose ports
EXPOSE 80/tcp
EXPOSE 443/tcp

# Copy init scripts
COPY rootfs /





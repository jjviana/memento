FROM ubuntu

RUN apt-get update && \
      apt-get -y install sudo

ENTRYPOINT [ "/bin/bash" ]

# Create the memento user home directory
RUN mkdir -p /home/memento
# Add a memento user with a home directory
RUN useradd -d /home/memento -s /usr/local/bin/memento-sh memento
# Change the owner of the memento user home directory
RUN chown memento:memento /home/memento
# Add the memento user to the sudoers group
RUN usermod -aG sudo memento

# Ensure sudo group users are not 
# asked for a password when using 
# sudo command by ammending sudoers file
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> \
/etc/sudoers

# Switch to the memento user
USER memento
# Set the working directory to the memento user home directory
WORKDIR /home/memento

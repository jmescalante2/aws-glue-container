FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

USER root 
RUN yum update -y && \
    yum install -y sudo && \
    yum clean all && \
    rm -rf /var/cache/yum 
RUN echo 'glue_user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/glue_user && \
    chmod 0440 /etc/sudoers.d/glue_user


USER glue_user
SHELL ["/bin/bash", "-c"]
RUN echo -e '\nsource /usr/share/bash-completion/completions/git' >> ~/.bashrc && source ~/.bashrc
RUN mkdir ~/.aws
RUN /home/glue_user/.local/bin/pip install poetry==1.6.1

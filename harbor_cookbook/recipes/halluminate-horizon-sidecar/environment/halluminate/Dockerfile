ARG HALLUMINATE_IMAGE=horizon-local-wyatt-test-problem-tagging:halluminate-horizon-e1ee7b24
FROM ${HALLUMINATE_IMAGE}

USER root

COPY serve_http.py /usr/local/bin/serve_http.py
RUN chmod +x /usr/local/bin/serve_http.py

EXPOSE 8000 6080

CMD ["bash", "/workdir/image/entrypoint.sh", "sh", "-lc", "cd /mcp_server && exec uv --offline --directory /mcp_server run python /usr/local/bin/serve_http.py"]

FROM freeradius/freeradius-server:latest
COPY raddb/ /etc/raddb/
RUN ln -s /etc/raddb/mods-available/sql /etc/raddb/mods-enabled/sql
RUN ln -s /etc/raddb/mods-available/sqlcounter /etc/raddb/mods-enabled/sqlcounter

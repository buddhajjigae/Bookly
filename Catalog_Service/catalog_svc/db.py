HOST = "milestonedb.crmw2ja3vleo.us-east-1.rds.amazonaws.com"
USER = "admin"

DB_URI = "mysql+pymysql://{}:{}@{}:3306/{}".format(
    USER, "comsw6156", HOST, "catalog_service"
)

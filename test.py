from utils import init_db, insertdb, viewdb

if __name__ == "__main__":
	init_db()
	insertdb("Rohith","Gangadhara","Asus FX505GE", "Dabba Service Centre", "Dabba Road, Dabba Cross, Dabba Layout, Dabbapura-560420")
	insertdb("Santosh","","HP FX505GE", "Dabba Service Centre", "Dabba Road, Dabba Cross, Dabba Layout, Dabbapura-560420")
	viewdb()
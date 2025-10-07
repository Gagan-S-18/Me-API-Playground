from database import Base, engine
import models  # <-- make sure this imports all your models

print("Creating all tables in meapi_playground.db...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")


from app import app, db
from models import ClientPolicy

with app.app_context():
   
    updated = ClientPolicy.query.filter(ClientPolicy.status == 'approved').update({"status": "active"})
    db.session.commit()
    print(f"{updated} policies updated from 'approved' to 'active'.")

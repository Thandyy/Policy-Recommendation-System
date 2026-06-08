from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

db = SQLAlchemy()

# Zimbabwe timezone
ZIMBABWE_TZ = pytz.timezone("Africa/Harare")

def now_zim():
    """Return current time in Zimbabwe timezone."""
    return datetime.now(ZIMBABWE_TZ)

# USER MODEL
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    # Relationships
    policies_created = db.relationship("Policy", backref="admin", lazy=True)
    policies_enrolled = db.relationship("ClientPolicy", backref="client", lazy=True)
    recommendations = db.relationship("PolicyRecommendation", backref="client", lazy=True)
    comments = db.relationship("Comment", backref="client", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"

# POLICY MODEL

class Policy(db.Model):
    __tablename__ = "policies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    eligibility_model = db.Column(db.String(250), nullable=True) 
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=now_zim)
    updated_at = db.Column(db.DateTime, default=now_zim, onupdate=now_zim)

    # Relationships
    plans = db.relationship("Plan", backref="policy", lazy=True, cascade="all, delete-orphan")
    updates = db.relationship("PolicyUpdate", backref="policy", lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship("PolicyRecommendation", backref="policy", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="policy", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Policy {self.name}>"

# PLAN MODEL

class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    premium_amount = db.Column(db.Numeric(10, 2), nullable=True)
    benefits = db.Column(db.Text, nullable=True)

    #client_policies = db.relationship("ClientPolicy", backref="plan", lazy=True)

    def __repr__(self):
        return f"<Plan {self.duration_months} months for Policy {self.policy_id}>"

# CLIENT POLICY MODEL

class ClientPolicy(db.Model):
    __tablename__ = "client_policies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)

    input_data = db.Column(db.JSON, nullable=False)
    predicted_eligible = db.Column(db.Boolean, nullable=False, default=False)
    confidence = db.Column(db.Float, nullable=True)

    status = db.Column(
        db.Enum("pending", "active", "rejected", "completed", name="policy_status"),
        default="pending"
    )
    applied_at = db.Column(db.DateTime, default=now_zim)

    # Add this relationship
    policy = db.relationship("Policy", backref="client_policies")

    def __repr__(self):
        return (
            f"<ClientPolicy user={self.user_id}, policy={self.policy_id}, "
            f"predicted_eligible={self.predicted_eligible}, status={self.status}>"
        )


# POLICY RECOMMENDATION MODEL
class PolicyRecommendation(db.Model):
    __tablename__ = "policy_recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=now_zim)

    def __repr__(self):
        return f"<Recommendation user={self.user_id}, policy={self.policy_id}>"

# POLICY UPDATE MODEL
class PolicyUpdate(db.Model):
    __tablename__ = "policy_updates"

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=now_zim)

    def __repr__(self):
        return f"<Update {self.title} for Policy {self.policy_id}>"

# COMMENT MODEL

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=now_zim)

    def __repr__(self):
        return f"<Comment user={self.user_id} policy={self.policy_id}>"

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        #db.drop_all()

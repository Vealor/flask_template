from .__model_imports import *
################################################################################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=True, server_default='t', nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    initials = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
    is_system_administrator = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    req_pass_reset = db.Column(db.Boolean, unique=False, default=True, server_default='t', nullable=False)

    user_projects = db.relationship('UserProject', back_populates='user_project_user', lazy='dynamic', passive_deletes=True)
    user_logs = db.relationship('Log', back_populates='log_user', lazy='dynamic')
    user_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_user', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'initials': self.initials.upper(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': "{} {}".format(self.first_name, self.last_name),
            'req_pass_reset': self.req_pass_reset,
            'role': self.role.name,
            'is_system_administrator': self.is_system_administrator,
            'is_superuser': self.is_superuser,
            'user_project_ids': [i.project_id for i in self.user_projects]
        }

    @property
    def serialize_user_proj(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'initials': self.initials.upper(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': "{} {}".format(self.first_name, self.last_name),
            'req_pass_reset': self.req_pass_reset,
            'role': self.role.name,
            'is_system_administrator': self.is_system_administrator,
            'is_superuser': self.is_superuser,
            'user_projects': [i.serialize for i in self.user_projects]
        }

    @classmethod
    def superuser_exists(cls):
        return cls.query.filter_by(is_superuser=True).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class UserProject(db.Model):
    __tablename__ = 'user_project'
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.UniqueConstraint('user_id', 'project_id', name='user_project_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True)
    is_favourite = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    user_id = db.Column(db.Integer, nullable=False) # FK
    user_project_user = db.relationship('User', back_populates='user_projects') # FK

    project_id = db.Column(db.Integer, nullable=False) # FK
    user_project_project = db.relationship('Project', back_populates='project_users') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user_project_user.username,
            'project_id': self.project_id,
            'project': self.user_project_project.serialize,
            'is_favourite': self.is_favourite
        }

class BlacklistToken(db.Model):
    __tablename__ = 'blacklisted_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

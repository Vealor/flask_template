from .__model_imports import *
################################################################################
class ParedownRule(db.Model):
    __tablename__ = 'paredown_rules'
    __table_args__ = (
        db.ForeignKeyConstraint(['paredown_rule_approver1_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['paredown_rule_approver2_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
        db.CheckConstraint('paredown_rule_approver1_id != paredown_rule_approver2_id'),
        db.CheckConstraint('is_core or (not is_core and not (bool(paredown_rule_approver1_id) or bool(paredown_rule_approver2_id)))'),
        db.CheckConstraint('((is_core and not coalesce(array_length(lob_sectors, 1), 0) > 0) or (not is_core and coalesce(array_length(lob_sectors, 1), 0) > 0))'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    comment = db.Column(db.String(128), nullable=True)

    lob_sectors = db.Column(ArrayOfEnum(postgresql.ENUM(LineOfBusinessSectors)), nullable=True)

    code_id = db.Column(db.Integer, nullable=False) # FK
    paredown_rule_code = db.relationship('Code', back_populates='code_paredown_rules')
    paredown_rule_approver1_id = db.Column(db.Integer, nullable=True) # FK
    paredown_rule_approver1_user = db.relationship('User', foreign_keys='ParedownRule.paredown_rule_approver1_id') # FK
    paredown_rule_approver2_id = db.Column(db.Integer, nullable=True) # FK
    paredown_rule_approver2_user = db.relationship('User', foreign_keys='ParedownRule.paredown_rule_approver2_id') # FK

    paredown_rule_conditions = db.relationship('ParedownRuleCondition', back_populates='paredown_rule_condition_paredown_rule', lazy='dynamic', passive_deletes=True) # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'is_core': self.is_core,
            'is_active': self.is_active,
            'conditions': [i.serialize for i in self.paredown_rule_conditions],
            'lob_sectors': self.lob_sectors if self.lob_sectors else [],
            'code': self.paredown_rule_code.serialize,
            'comment': self.comment,
            'approver1_id': self.paredown_rule_approver1_id,
            'approver1_username': self.paredown_rule_approver1_user.username if self.paredown_rule_approver1_id else None,
            'approver2_id': self.paredown_rule_approver2_id,
            'approver2_username': self.paredown_rule_approver2_user.username if self.paredown_rule_approver2_id else None
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ParedownRuleCondition(db.Model):
    __tablename__ = 'paredown_rules_conditions'
    __table_args__ = (
        db.ForeignKeyConstraint(['paredown_rule_id'], ['paredown_rules.id'], ondelete='CASCADE'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    field = db.Column(db.String(128), nullable=False)
    operator = db.Column(db.String(128), nullable=False)
    value = db.Column(db.String(128), nullable=False)

    paredown_rule_id = db.Column(db.Integer, nullable=False) # FK
    paredown_rule_condition_paredown_rule = db.relationship('ParedownRule', back_populates='paredown_rule_conditions') #FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'field': self.field,
            'paredown_rule_id': self.paredown_rule_id,
            'operator': self.operator,
            'value': self.value
        }

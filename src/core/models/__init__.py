from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# CORE
from ._enums import *  # noqa: E402, F401, F403
from .auth import *  # noqa: E402, F401, F403
from .cdm_labels import *  # noqa: E402, F401, F403
from .clients import *  # noqa: E402, F401, F403
from .data_mappings import *  # noqa: E402, F401, F403
from .data_params import *  # noqa: E402, F401, F403
from .logs import *  # noqa: E402, F401, F403
from .projects import *  # noqa: E402, F401, F403
from .users import *  # noqa: E402, F401, F403

# ROYALTIES
